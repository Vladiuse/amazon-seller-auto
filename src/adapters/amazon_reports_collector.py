import logging
import os
from datetime import datetime

import requests as req
from requests.exceptions import RequestException
from sp_api.api import Reports
from sp_api.base import Marketplaces, ProcessingStatus, ReportType
from sp_api.base.exceptions import SellingApiRequestThrottledException

from src.application.amazon.amazon_report_product_collector.dto.report import AmazonReport, ReportDocument
from src.application.amazon.amazon_report_product_collector.interfaces.amazon_reports_collector import (
    IAmazonReportCollector,
)
from src.application.amazon.utils import retry
from src.main.config import credentials
from src.main.exceptions import ReportDocumentNotComplete, ReportStatusError


class AmazonReportCollector(IAmazonReportCollector):

    def __init__(self, marketplace: Marketplaces):
        self.marketplace = marketplace
        self.reports = Reports(credentials=credentials, marketplace=marketplace)

    @retry(
        attempts=5,
        delay=3 * 60,
        exceptions=[SellingApiRequestThrottledException, ],
    )
    def create_report(self, report_type: ReportType) -> str:
        data = self.reports.create_report(reportType=report_type)
        logging.info(data.payload)
        return data.payload['reportId']

    @retry(
        attempts=3,
        delay=10,
        exceptions=[SellingApiRequestThrottledException],
    )
    def get_today_reports(self, report_type: ReportType) -> list[AmazonReport]:
        date = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0).isoformat()
        data = self.reports.get_reports(
            reportTypes=[report_type, ],
            processingStatuses=[ProcessingStatus.DONE, ],
            createdSince=date,
        )
        logging.info(data.payload)
        return [AmazonReport(**report_data) for report_data in data.payload['reports']]

    def get_exiting_report(self, report_type: ReportType) -> AmazonReport | None:
        reports = self.get_today_reports(report_type=report_type)
        if reports:
            return max(reports, key=lambda report: report.created)
        return None

    @retry(
        attempts=20,
        delay=30,
        exceptions=[ReportDocumentNotComplete, ],
    )
    def get_report(self, report_id: str) -> AmazonReport:
        data = self.reports.get_report(reportId=report_id)
        logging.info(data.payload)
        report = AmazonReport(**data.payload)
        if report.is_complete():
            if report.is_document_created():
                return AmazonReport(**data.payload)
            raise ReportStatusError
        logging.error(data.payload)
        logging.error('report not complete')
        raise ReportDocumentNotComplete

    def get_report_document(self, document_id: str) -> ReportDocument:
        data = self.reports.get_report_document(reportDocumentId=document_id)
        return ReportDocument(**data.payload)

    @retry(
        attempts=5,
        delay=10,
        exceptions=[RequestException, ],
    )
    def get_report_document_text(self, report_document_url: str) -> str:
        res = req.get(report_document_url)
        res.raise_for_status()
        return res.text

    @retry(
        attempts=3,
        delay=1,
        exceptions=[ReportStatusError, ],
    )
    def create_and_get_report_text(self, report_type: ReportType) -> str:
        report = self.get_exiting_report(report_type=report_type)
        logging.info('Get exiting report')
        if report is None:
            report_id = self.create_report(report_type=report_type)
            report = self.get_report(report_id=report_id)
        report_document = self.get_report_document(document_id=report.document_id)
        return self.get_report_document_text(report_document.url)

    # TODO тут я выполняю цезочку запросов, дейстивой чтоб создать отчет
    # в этом классе норм это расположить или в какой другой вынести?
    # и теоретически может возникнуть ситуация что report не создаться или создаться с
    # статусом Fail на всех попытках - я не понимаю что в таком случае делать.


class AmazonSavedReportCollector(AmazonReportCollector):

    def create_and_get_report_text(self, report_type: ReportType) -> str:
        geo = str(self.marketplace).split('.')[-1]
        file_name = f'{geo}_{report_type.value}.txt'
        file_path = os.path.join('media/reports', file_name)
        with open(file_path) as file:
            return file.read()
