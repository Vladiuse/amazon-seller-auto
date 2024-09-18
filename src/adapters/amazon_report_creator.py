import logging

from sp_api.api import Reports as SpApiReports
from sp_api.base import ReportType
from sp_api.base.exceptions import SellingApiRequestThrottledException

from src.application.amazon.amazon_report_product_collector.dto.report import AmazonReportProduct
from src.application.amazon.amazon_report_product_collector.interfaces.amazon_report_creator import (
    IAmazonReport,
    IAmazonReportCreator,
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


class AmazonReport(IAmazonReport):

    def __init__(self, sp_api_reports: SpApiReports):
        self.sp_api_reports = sp_api_reports

    @retry(
        attempts=20,
        delay=30,
        exceptions=(ReportDocumentNotComplete,),
    )
    def get_report(self, report_id: str) -> AmazonReportProduct:
        data = self.sp_api_reports.get_report(reportId=report_id)
        logging.info(data.payload)
        report = AmazonReportProduct(**data.payload)
        if report.is_complete():
            if report.is_document_created():
                return AmazonReportProduct(**data.payload)
            raise ReportStatusError
        logging.error('Report not complete \n %s', data.payload)
        raise ReportDocumentNotComplete
