import logging
from datetime import datetime

import requests
from requests.exceptions import RequestException
from sp_api.api import Reports as SpApiReports
from sp_api.base import ProcessingStatus, ReportType
from sp_api.base.exceptions import SellingApiRequestThrottledException

from src.application.amazon.amazon_report_product_collector.dto.report import AmazonReport, ReportDocument
from src.application.amazon.amazon_report_product_collector.interfaces.amazon_report import (
    IAmazonReportCreator,
    IAmazonReportDocumentGetter,
    IAmazonReportGetter,
)
from src.application.amazon.utils import retry
from src.main.exceptions import ReportDocumentNotComplete, ReportStatusError


class AmazonReportCreator(IAmazonReportCreator):

    def __init__(self, sp_api_reports: SpApiReports):
        self.sp_api_reports = sp_api_reports

    @retry(
        attempts=5,
        delay=3 * 60,
        exceptions=(SellingApiRequestThrottledException,),
    )
    def create_report(self, report_type: ReportType) -> str:
        data = self.sp_api_reports.create_report(reportType=report_type)
        logging.info(data.payload)
        return data.payload['reportId']


class AmazonReportGetter(IAmazonReportGetter):

    def __init__(self, sp_api_reports: SpApiReports):
        self._sp_api_reports = sp_api_reports

    @retry(
        attempts=20,
        delay=30,
        exceptions=(ReportDocumentNotComplete,),
    )
    def get_report(self, report_id: str) -> AmazonReport:
        data = self._sp_api_reports.get_report(reportId=report_id)
        logging.info(data.payload)
        report = AmazonReport(**data.payload)
        if not report.is_complete():
            raise ReportDocumentNotComplete
        if report.is_document_created():
            return AmazonReport(**data.payload)
        logging.error('Report not created \n %s', data.payload)
        raise ReportStatusError

    @retry(
        attempts=3,
        delay=10,
        exceptions=(SellingApiRequestThrottledException,),
    )
    def get_today_reports(self, report_type: ReportType) -> list[AmazonReport]:
        date = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0).isoformat()
        data = self._sp_api_reports.get_reports(
            reportTypes=[report_type, ],
            processingStatuses=[ProcessingStatus.DONE, ],
            createdSince=date,
        )
        logging.info(data.payload)
        return [AmazonReport(**report_data) for report_data in data.payload['reports']]


class AmazonReportDocumentGetter(IAmazonReportDocumentGetter):

    def __init__(self, sp_api_reports: SpApiReports):
        self.sp_api_reports = sp_api_reports

    @retry(
        attempts=3,
        delay=20,
        exceptions=(SellingApiRequestThrottledException,),
    )
    def get_report_document(self, document_id: str) -> ReportDocument:
        data = self.sp_api_reports.get_report_document(reportDocumentId=document_id)
        return ReportDocument(**data.payload)

    @retry(
        attempts=3,
        delay=15,
        exceptions=(RequestException,),
    )
    def get_report_document_text(self, document_url: str) -> str:
        response = requests.get(document_url)
        response.raise_for_status()
        return response.text
