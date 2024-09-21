import logging
from dataclasses import dataclass

from src.application.amazon.reports.dto.report import AmazonReportDocument
from src.application.amazon.reports.interfaces.report import (
    IAmazonReportCreator,
    IAmazonReportDocumentGetter,
    IAmazonReportGetter,
)
from src.application.amazon.reports.interfaces.report_documents_provider import (
    IAmazonReportProvider,
)
from src.application.amazon.reports.types import ReportType


@dataclass
class AmazonReportDocumentProvider(IAmazonReportProvider):
    report_creator: IAmazonReportCreator
    report_getter: IAmazonReportGetter
    report_document_getter: IAmazonReportDocumentGetter

    def provide(self, report_type: ReportType, try_get_exists_report: bool = False, **kwargs) -> AmazonReportDocument:
        if try_get_exists_report:
            exiting_reports = self.report_getter.get_today_reports(report_type=report_type)
            if len(exiting_reports) != 0:
                report = max(exiting_reports, key=lambda report: report.created)
                logging.info('Get exiting report %s', report_type.value)
                return self.report_document_getter.get_report_document(document_id=report.document_id)
        logging.info('Try create report %s', report_type.value)
        report_id = self.report_creator.create_report(report_type=report_type, **kwargs)
        report = self.report_getter.get_report(report_id=report_id)
        return self.report_document_getter.get_report_document(document_id=report.document_id)
