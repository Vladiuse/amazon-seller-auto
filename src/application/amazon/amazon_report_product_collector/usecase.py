import logging

from sp_api.api import Reports as SpApiReports
from sp_api.base import ReportType

from src.application.amazon.amazon_report_product_collector.dto.report import AmazonReport
from src.application.amazon.amazon_report_product_collector.interfaces.amazon_report_creator import (
    IAmazonReportCreator,
    IAmazonReportGetter,
)
from src.application.amazon.utils import retry
from src.main.exceptions import ReportStatusError


class CreateAmazonReportUseCase:

    def __init__(self,
                 sp_api_reports: SpApiReports,
                 report_creator: IAmazonReportCreator,
                 report_getter: IAmazonReportGetter,
                 ):
        self._sp_api_reports = sp_api_reports
        self._report_creator = report_creator
        self._report_getter = report_getter

    @retry(
        attempts=3,
        delay=60,
        exceptions=(ReportStatusError,),
    )
    def create_report(self, report_type: ReportType) -> AmazonReport:
        report_id = self._report_creator.create_report(report_type=report_type)
        return self._report_getter.get_report(report_id=report_id)


class GetExitingAmazonReportsUseCase:

    def __init__(self,
                 sp_api_reports: SpApiReports,
                 report_getter: IAmazonReportGetter,
                 ):
        self._sp_api_reports = sp_api_reports
        self._report_getter = report_getter

    def get_exiting_report(self, report_type: ReportType) -> AmazonReport | None:
        reports = self._report_getter.get_today_reports(report_type=report_type)
        if len(reports) != 0:
            return max(reports, key=lambda report: report.created)
        return None


class GetExitingOrCreateAmazonReportUseCase:

    def __init__(self,
                 sp_api_reports: SpApiReports,
                 report_creator: IAmazonReportCreator,
                 report_getter: IAmazonReportGetter,
                 ):
        self._sp_api_reports = sp_api_reports
        self._report_creator = report_creator
        self._report_getter = report_getter

    def get_or_create_report(self, report_type: ReportType) -> AmazonReport:
        exiting_report = GetExitingAmazonReportsUseCase(
            sp_api_reports=self._sp_api_reports,
            report_getter=self._report_getter,
        ).get_exiting_report(report_type=report_type)
        if exiting_report is not None:
            logging.info('Get exiting report')
            return exiting_report
        return CreateAmazonReportUseCase(
            sp_api_reports=self._sp_api_reports,
            report_creator=self._report_creator,
            report_getter=self._report_getter,
        ).create_report(report_type=report_type)
