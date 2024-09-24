import logging
from dataclasses import dataclass

from src.application.amazon.common.types import MarketplaceCountry
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

    def provide(self,
                credentials: dict,
                marketplace_country: MarketplaceCountry,
                report_type: ReportType,
                try_get_exists_report: bool = False,
                **kwargs,
                ) -> AmazonReportDocument:
        if try_get_exists_report:
            exiting_reports = self.report_getter.get_today_reports(credentials=credentials, report_type=report_type,
                                                                   marketplace_country=marketplace_country)
            if len(exiting_reports) != 0:
                report = max(exiting_reports, key=lambda report: report.created)
                logging.info('Get exiting report %s', report_type.value)
                return self.report_document_getter.get_report_document(credentials=credentials,
                                                                       document_id=report.document_id,
                                                                       marketplace_country=marketplace_country)
        logging.info('Try create report %s', report_type.value)
        report_id = self.report_creator.create_report(credentials=credentials, marketplace_country=marketplace_country,
                                                      report_type=report_type,
                                                      **kwargs)
        report = self.report_getter.get_report(credentials=credentials, marketplace_country=marketplace_country,
                                               report_id=report_id)
        return self.report_document_getter.get_report_document(credentials=credentials, document_id=report.document_id,
                                                               marketplace_country=marketplace_country)
