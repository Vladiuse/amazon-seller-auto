import logging

from sp_api.api import Reports as SpApiReports
from sp_api.base import ReportType
from sp_api.base.exceptions import SellingApiRequestThrottledException

from src.application.amazon.amazon_report_product_collector.interfaces.amazon_report_creator import IAmazonReportCreator
from src.application.amazon.utils import retry


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
