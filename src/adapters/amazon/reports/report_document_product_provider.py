import gzip
import os
from dataclasses import dataclass
from datetime import datetime

from src.adapters.amazon.reports.report_document_product_converter import (
    InventoryReportDocumentConverter,
    SalesReportDocumentConvertor,
    VendorSalesReportConverter,
)
from src.application.amazon.common.interfaces.amazon_request_sender import (
    IAmazonRequestSender,
)
from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.reports.dto.product import (
    AmazonInventoryReportProduct,
    SaleReportProduct,
    VendorSaleProduct,
)
from src.application.amazon.reports.interfaces.report_document_product_provider import (
    IAmazonReportDocumentProductProvider,
)
from src.application.amazon.reports.interfaces.report_documents_provider import IAmazonReportProvider
from src.application.amazon.reports.types import ReportType
from src.application.amazon.utils import save_amazon_report
from src.main.config import REPORTS_DIR, config

amazon_seller_credentials = {
    'refresh_token': config.amazon_config.SELLER_SP_API_REFRESH_TOKEN,
    'lwa_app_id': config.amazon_config.SELLER_LWA_CLIENT_ID,
    'lwa_client_secret': config.SELLER_amazon_config.LWA_CLIENT_SECRET,
}

amazon_vendor_credentials = {
    'refresh_token': config.amazon_config.VENDOR_SP_API_REFRESH_TOKEN,
    'lwa_app_id': config.amazon_config.VENDOR_SELLER_LWA_CLIENT_ID,
    'lwa_client_secret': config.SELLER_amazon_config.VENDOR_LWA_CLIENT_SECRET,
}


@dataclass
class AmazonInventoryReportDocumentProductProvider(IAmazonReportDocumentProductProvider):
    amazon_request_sender: IAmazonRequestSender
    amazon_report_document_provider: IAmazonReportProvider

    def provide(self, marketplace_country: MarketplaceCountry) -> list[AmazonInventoryReportProduct]:
        report_type = ReportType.INVENTORY
        report_document = self.amazon_report_document_provider.provide(
            marketplace_country=marketplace_country,
            report_type=report_type,
            try_get_exists_report=True,
            credentials=amazon_seller_credentials,
        )
        report_document_content = self.amazon_request_sender.get(report_document.url)
        report_document_text = report_document_content.decode('utf-8')
        save_amazon_report(
            report_document_text=report_document_text,
            marketplace_country=marketplace_country,
            report_type=report_type,
            output_file_format='csv',
        )
        inventory_report_converter = InventoryReportDocumentConverter()
        return inventory_report_converter.convert(report_document_text=report_document_text,
                                                  marketplace_country=marketplace_country)


class InventoryReportProviderFromFile(IAmazonReportDocumentProductProvider):

    def __init__(self, *args, **kwargs):
        pass

    def provide(self, marketplace_country: MarketplaceCountry) -> list[AmazonInventoryReportProduct]:
        report_file_name = f'{marketplace_country.value}_{ReportType.INVENTORY.value.value}.csv'
        report_path = os.path.join(REPORTS_DIR, report_file_name)
        with open(report_path) as file:
            report_document_text = file.read()
        inventory_report_converter = InventoryReportDocumentConverter()
        return inventory_report_converter.convert(report_document_text=report_document_text,
                                                  marketplace_country=marketplace_country)


@dataclass
class AmazonSalesReportDocumentProductProvider(IAmazonReportDocumentProductProvider):
    amazon_request_sender: IAmazonRequestSender
    amazon_report_document_provider: IAmazonReportProvider

    def provide(self, marketplace_country: MarketplaceCountry) -> list[SaleReportProduct]:
        report_type = ReportType.SALES
        report_document = self.amazon_report_document_provider.provide(
            credentials=amazon_seller_credentials,
            marketplace_country=marketplace_country,
            report_type=report_type,
            reportOptions={"dateGranularity": "MONTH", "asinGranularity": "SKU"},
        )
        report_document_content = self.amazon_request_sender.get(report_document.url)
        report_document_text = gzip.decompress(report_document_content).decode('utf-8')
        save_amazon_report(
            report_document_text=report_document_text,
            marketplace_country=marketplace_country,
            report_type=report_type,
            output_file_format='json',
        )
        sales_report_converter = SalesReportDocumentConvertor()
        return sales_report_converter.convert(report_document_text=report_document_text,
                                              marketplace_country=marketplace_country)


class SalesReportProviderFromFile(IAmazonReportDocumentProductProvider):

    def __init__(self, *args, **kwargs):
        pass

    def provide(self, marketplace_country: MarketplaceCountry) -> list[SaleReportProduct]:
        report_file_name = f'{marketplace_country.value}_{ReportType.SALES.value.value}.json'
        report_path = os.path.join(REPORTS_DIR, report_file_name)
        with open(report_path) as file:
            report_document_text = file.read()
        sales_report_converter = SalesReportDocumentConvertor()
        return sales_report_converter.convert(report_document_text=report_document_text,
                                              marketplace_country=marketplace_country)


@dataclass
class AmazonVendorSalesReportDocumentProductProvider(IAmazonReportDocumentProductProvider):
    amazon_report_document_provider: IAmazonReportProvider
    amazon_request_sender: IAmazonRequestSender

    def provide(self, marketplace_country: MarketplaceCountry) -> list[VendorSaleProduct]:
        report_type = ReportType.VENDOR_SALES
        start_date = datetime(2024, 9, 23).isoformat()
        end_date = datetime(2024, 9, 24).isoformat()
        report_document = self.amazon_report_document_provider.provide(
            credentials=amazon_vendor_credentials,
            marketplace_country=marketplace_country,
            report_type=report_type,
            dataStartTime=start_date,
            dataEndTime=end_date,
        )
        report_document_content = self.amazon_request_sender.get(report_document.url)
        report_document_text = gzip.decompress(report_document_content).decode('utf-8')
        save_amazon_report(
            report_document_text=report_document_text,
            marketplace_country=marketplace_country,
            report_type=report_type,
            output_file_format='json',
        )
        sales_report_converter = VendorSalesReportConverter()
        return sales_report_converter.convert(report_document_text=report_document_text,
                                              marketplace_country=marketplace_country)


class VendorSalesReportProviderFromFile(IAmazonReportDocumentProductProvider):

    def __init__(self, *args, **kwargs):
        pass

    def provide(self, marketplace_country: MarketplaceCountry) -> list[VendorSaleProduct]:
        report_file_name = f'{marketplace_country.value}_{ReportType.VENDOR_SALES.value.value}.json'
        report_path = os.path.join(REPORTS_DIR, report_file_name)
        with open(report_path) as file:
            report_document_text = file.read()
        sales_report_converter = VendorSalesReportConverter()
        return sales_report_converter.convert(report_document_text=report_document_text,
                                              marketplace_country=marketplace_country)
