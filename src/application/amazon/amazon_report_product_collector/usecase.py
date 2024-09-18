import logging
from dataclasses import dataclass

from sp_api.api import Reports
from sp_api.base import Marketplaces, ReportType

from src.adapters.amazon_report_creator import AmazonReportCreator, AmazonReportDocumentGetter, AmazonReportGetter
from src.adapters.amazon_report_product_converter import ReportProductConverter
from src.adapters.amazon_report_products_collector import AmazonReportProductsCollector
from src.adapters.amazon_reports_collector import AmazonReportDocumentTextCollector, AmazonSavedReportDocumentReader
from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct
from src.main.config import config


@dataclass
class CollectFBAInventoryReportProductsUseCase:

    def collect(self, marketplaces: list[Marketplaces]) -> list[AmazonReportProduct]:
        amazon_credentials = {
            'refresh_token': config.amazon_config.SP_API_REFRESH_TOKEN,
            'lwa_app_id': config.amazon_config.LWA_CLIENT_ID,
            'lwa_client_secret': config.amazon_config.LWA_CLIENT_SECRET,
        }
        report_type = ReportType.GET_FBA_MYI_ALL_INVENTORY_DATA
        products = []
        for marketplace in marketplaces:
            sp_api_reports = Reports(credentials=amazon_credentials, marketplace=marketplace)
            reports_getter = AmazonReportGetter(sp_api_reports=sp_api_reports)
            report_creator = AmazonReportCreator(sp_api_reports=sp_api_reports)
            report_document_getter = AmazonReportDocumentGetter(sp_api_reports=sp_api_reports)
            report_text_collector = AmazonReportDocumentTextCollector(
                sp_api_reports=sp_api_reports,
                report_creator=report_creator,
                report_getter=reports_getter,
                report_document_getter=report_document_getter,
            )
            report_convertor = ReportProductConverter()
            report_product_collector = AmazonReportProductsCollector(
                report_convertor=report_convertor,
                # report_collector=report_text_collector,
                report_collector=AmazonSavedReportDocumentReader(sp_api_reports=sp_api_reports),  # TEST
            )
            report_products = report_product_collector.collect(report_type=report_type, marketplace=marketplace)
            logging.info('On %s collected: %s', marketplace, len(report_products))
            products.extend(report_products)
        return products
