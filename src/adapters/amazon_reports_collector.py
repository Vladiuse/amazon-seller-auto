import logging
import os
from dataclasses import dataclass

from sp_api.api import Reports as SpApiReports
from sp_api.base import ReportType as SpReportType, Marketplaces as SpMarketplaces
from src.application.amazon.amazon_reports.dto.product import AmazonReportProduct

from src.application.amazon.amazon_reports.types import ReportType
from src.application.amazon.amazon_reports.dto.report import AmazonReportDocument
from src.application.amazon.amazon_reports.interfaces.amazon_report import (
    IAmazonReportCreator,
    IAmazonReportDocumentGetter,
    IAmazonReportGetter,
)
from src.application.amazon.amazon_reports.interfaces.amazon_reports_collector import (
    IAmazonReportProvider,
    IAmazonReportDocumentProductProvider,
)
from src.application.amazon.common.interfaces.amazon_request_sender import (
    IAmazonRequestSender,
)
from src.main.config import REPORTS_DIR
from src.application.amazon.utils import save_amazon_report, get_marketplace_country
from src.adapters.amazon_report_product_converter import FBAReportDocumentConverter


@dataclass
class AmazonReportDocumentProvider(IAmazonReportProvider):
    report_creator: IAmazonReportCreator
    report_getter: IAmazonReportGetter
    report_document_getter: IAmazonReportDocumentGetter

    def provide(self, report_type: ReportType, **kwargs) -> AmazonReportDocument:
        exiting_reports = self.report_getter.get_today_reports(report_type=report_type)
        if len(exiting_reports) != 0:
            report = max(exiting_reports, key=lambda report: report.created)
            logging.info('Get exiting report %s', report_type.value)
        else:
            report_id = self.report_creator.create_report(report_type=report_type, **kwargs)
            report = self.report_getter.get_report(report_id=report_id)
        return self.report_document_getter.get_report_document(document_id=report.document_id)


@dataclass
class AmazonInventoryReportDocumentProductProvider(IAmazonReportDocumentProductProvider):
    amazon_request_sender: IAmazonRequestSender
    amazon_report_document_provider: IAmazonReportProvider

    def collect(self, report_document: AmazonReportDocument, marketplace: SpMarketplaces) -> list[AmazonReportProduct]:
        report_type = ReportType.INVENTORY
        marketplace_country = get_marketplace_country(marketplace)
        report_document = self.amazon_report_document_provider.provide(
            report_type=report_type,
        )
        report_document_content = self.amazon_request_sender.get(report_document.url)
        report_document_text = report_document_content.decode('utf-8')
        save_amazon_report(
            report_document_text=report_document_text,
            marketplace_country=marketplace_country,
            report_type=report_type,
        )
        converter = FBAReportDocumentConverter()
        return converter.convert(report_document_text=report_document_text, marketplace_country=marketplace_country)


