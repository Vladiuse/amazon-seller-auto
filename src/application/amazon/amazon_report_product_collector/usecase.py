import logging
from datetime import datetime

import requests
from requests.exceptions import RequestException
from sp_api.api import Reports as SpApiReports
from sp_api.base import ProcessingStatus, ReportType
from sp_api.base.exceptions import SellingApiRequestThrottledException

from src.application.amazon.amazon_report_product_collector.dto.report import AmazonReportProduct
from src.application.amazon.utils import retry


class GetExitingAmazonReportsUseCase:

    def __init__(self, sp_api_reports: SpApiReports):
        self.sp_api_reports = sp_api_reports

    @retry(
        attempts=3,
        delay=10,
        exceptions=(SellingApiRequestThrottledException,),
    )
    def __get_today_reports(self, report_type: ReportType) -> list[AmazonReportProduct]:
        date = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0).isoformat()
        data = self.sp_api_reports.get_reports(
            reportTypes=[report_type, ],
            processingStatuses=[ProcessingStatus.DONE, ],
            createdSince=date,
        )
        logging.info(data.payload)
        return [AmazonReportProduct(**report_data) for report_data in data.payload['reports']]

    def get_exiting_report(self, report_type: ReportType) -> AmazonReportProduct | None:
        reports = self.__get_today_reports(report_type=report_type)
        if len(reports) != 0:
            return max(reports, key=lambda report: report.created)
        return None


class GetAmazonReportDocumentTextUseCase:

    @retry(
        attempts=5,
        delay=10,
        exceptions=(RequestException,),
    )
    def get_text(self, report_document_url: str) -> str:
        response = requests.get(report_document_url)
        response.raise_for_status()
        return response.text
