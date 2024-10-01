import gzip
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from src.application.amazon.common.interfaces.amazon_request_sender import (
    IAmazonRequestSender,
)
from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.reports.dto.product import (
    AmazonInventoryReportProduct,
    FeeAmazonProduct,
    ReservedProduct,
    SaleReportProduct,
    VendorSaleProduct,
    SalesRankProduct,
)
from src.application.amazon.reports.interfaces.report_document_product_provider import (
    IAmazonReportDocumentProductProvider,
)
from src.application.amazon.reports.interfaces.report_documents_provider import IAmazonReportProvider
from src.application.amazon.reports.interfaces.report_product_converter import (
    IFeeReportConverter,
    IInventoryReportConverter,
    IReservedReportConverter,
    ISalesReportConverter,
    IVendorSalesReportConverter,
    ISalesRankReportConvertor,
)
from src.application.amazon.reports.types import ReportType
from src.application.amazon.utils import read_amazon_report, save_amazon_report
from src.main.config import config
from src.main.exceptions import ReportStatusError

amazon_seller_credentials = {
    'refresh_token': config.amazon_config.SELLER_SP_API_REFRESH_TOKEN,
    'lwa_app_id': config.amazon_config.SELLER_LWA_CLIENT_ID,
    'lwa_client_secret': config.amazon_config.SELLER_LWA_CLIENT_SECRET,
}

amazon_vendor_credentials = {
    'refresh_token': config.amazon_config.VENDOR_SP_API_REFRESH_TOKEN,
    'lwa_app_id': config.amazon_config.VENDOR_LWA_CLIENT_ID,
    'lwa_client_secret': config.amazon_config.VENDOR_LWA_CLIENT_SECRET,
}


@dataclass
class AmazonInventoryReportDocumentProductProvider(IAmazonReportDocumentProductProvider):
    amazon_request_sender: IAmazonRequestSender
    amazon_report_document_provider: IAmazonReportProvider
    amazon_report_product_converter: IInventoryReportConverter

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
        return self.amazon_report_product_converter.convert(report_document_text=report_document_text,
                                                            marketplace_country=marketplace_country)


@dataclass
class InventoryReportProviderFromFile(IAmazonReportDocumentProductProvider):
    amazon_report_product_converter: IInventoryReportConverter

    def provide(self, marketplace_country: MarketplaceCountry) -> list[AmazonInventoryReportProduct]:
        report_document_text = read_amazon_report(
            report_type=ReportType.INVENTORY,
            marketplace_country=marketplace_country,
            file_format='csv',
        )
        return self.amazon_report_product_converter.convert(report_document_text=report_document_text,
                                                            marketplace_country=marketplace_country)


@dataclass
class AmazonSalesReportDocumentProductProvider(IAmazonReportDocumentProductProvider):
    amazon_request_sender: IAmazonRequestSender
    amazon_report_document_provider: IAmazonReportProvider
    amazon_report_product_converter: ISalesReportConverter

    def provide(self, marketplace_country: MarketplaceCountry) -> list[SaleReportProduct]:
        report_type = ReportType.SALES
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        report_document = self.amazon_report_document_provider.provide(
            credentials=amazon_seller_credentials,
            marketplace_country=marketplace_country,
            report_type=report_type,
            dataStartTime=yesterday.isoformat(),
            dataEndTime=today.isoformat(),
            reportOptions={
                "asinGranularity": "SKU",
            },
        )
        report_document_content = self.amazon_request_sender.get(report_document.url)
        report_document_text = gzip.decompress(report_document_content).decode('utf-8')
        save_amazon_report(
            report_document_text=report_document_text,
            marketplace_country=marketplace_country,
            report_type=report_type,
            output_file_format='json',
        )
        return self.amazon_report_product_converter.convert(report_document_text=report_document_text,
                                                            marketplace_country=marketplace_country)


@dataclass
class SalesReportProviderFromFile(IAmazonReportDocumentProductProvider):
    amazon_report_product_converter: ISalesReportConverter

    def provide(self, marketplace_country: MarketplaceCountry) -> list[SaleReportProduct]:
        report_document_text = read_amazon_report(
            report_type=ReportType.SALES,
            marketplace_country=marketplace_country,
            file_format='json',
        )
        return self.amazon_report_product_converter.convert(report_document_text=report_document_text,
                                                            marketplace_country=marketplace_country)


@dataclass
class AmazonVendorSalesReportDocumentProductProvider(IAmazonReportDocumentProductProvider):
    amazon_report_document_provider: IAmazonReportProvider
    amazon_request_sender: IAmazonRequestSender
    amazon_report_product_converter: IVendorSalesReportConverter

    def provide(self, marketplace_country: MarketplaceCountry) -> list[VendorSaleProduct]:
        report_type = ReportType.VENDOR_SALES
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        report_document = self.amazon_report_document_provider.provide(
            credentials=amazon_vendor_credentials,
            marketplace_country=marketplace_country,
            report_type=report_type,
            dataStartTime=yesterday.isoformat(),
            dataEndTime=today.isoformat(),
        )
        report_document_content = self.amazon_request_sender.get(report_document.url)
        report_document_text = gzip.decompress(report_document_content).decode('utf-8')
        save_amazon_report(
            report_document_text=report_document_text,
            marketplace_country=marketplace_country,
            report_type=report_type,
            output_file_format='json',
        )
        return self.amazon_report_product_converter.convert(report_document_text=report_document_text,
                                                            marketplace_country=marketplace_country)


@dataclass
class VendorSalesReportProviderFromFile(IAmazonReportDocumentProductProvider):
    amazon_report_product_converter: IVendorSalesReportConverter

    def provide(self, marketplace_country: MarketplaceCountry) -> list[VendorSaleProduct]:
        report_document_text = read_amazon_report(
            report_type=ReportType.VENDOR_SALES,
            marketplace_country=marketplace_country,
            file_format='json',
        )
        return self.amazon_report_product_converter.convert(report_document_text=report_document_text,
                                                            marketplace_country=marketplace_country)


@dataclass
class FeeReportDocumentProvider(IAmazonReportDocumentProductProvider):
    amazon_request_sender: IAmazonRequestSender
    amazon_report_document_provider: IAmazonReportProvider
    amazon_report_product_converter: IFeeReportConverter 

    def provide(self, marketplace_country: MarketplaceCountry) -> list[FeeAmazonProduct]:
        report_type = ReportType.FEE
        report_document = self.amazon_report_document_provider.provide(
            marketplace_country=marketplace_country,
            report_type=report_type,
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
        return self.amazon_report_product_converter.convert(report_document_text=report_document_text)


@dataclass
class FeeReportProviderFromFile(IAmazonReportDocumentProductProvider):
    amazon_report_product_converter: IFeeReportConverter

    def provide(self, marketplace_country: MarketplaceCountry) -> list[FeeAmazonProduct]:
        report_document_text = read_amazon_report(
            report_type=ReportType.FEE,
            marketplace_country=marketplace_country,
            file_format='csv',
        )
        return self.amazon_report_product_converter.convert(report_document_text=report_document_text)

@dataclass
class ReservedReportProductProvider(IAmazonReportDocumentProductProvider):
    amazon_request_sender: IAmazonRequestSender
    amazon_report_document_provider: IAmazonReportProvider
    amazon_report_product_converter:  IReservedReportConverter

    def provide(self, marketplace_country: MarketplaceCountry) -> list[ReservedProduct]:
        report_type = ReportType.RESERVED
        try:
            report_document = self.amazon_report_document_provider.provide(
                marketplace_country=marketplace_country,
                report_type=report_type,
                credentials=amazon_seller_credentials,
            )
        except ReportStatusError:  # amazon have limits, need wait more than hour
            logging.error('ReportStatusError: %s %s', marketplace_country, report_type)
            return []
        report_document_content = self.amazon_request_sender.get(report_document.url)
        report_document_text = report_document_content.decode('utf-8')
        save_amazon_report(
            report_document_text=report_document_text,
            marketplace_country=marketplace_country,
            report_type=report_type,
            output_file_format='csv',
        )
        return self.amazon_report_product_converter.convert(report_document_text=report_document_text,
                                                            marketplace_country=marketplace_country)


@dataclass
class ReservedReportProductProviderFromFile(IAmazonReportDocumentProductProvider):
    amazon_report_product_converter: IReservedReportConverter

    def provide(self, marketplace_country: MarketplaceCountry) -> list[ReservedProduct]:
        report_type = ReportType.RESERVED
        try:
            report_document_text = read_amazon_report(
                report_type=report_type,
                marketplace_country=marketplace_country,
                file_format='csv',
            )
            return self.amazon_report_product_converter.convert(report_document_text=report_document_text,
                                                                marketplace_country=marketplace_country)
        except FileNotFoundError:
            logging.error('ReportStatusError: %s %s', marketplace_country, report_type)
            return []

@dataclass
class SalesRankReportProductProvider(IAmazonReportDocumentProductProvider):
    amazon_request_sender: IAmazonRequestSender
    amazon_report_document_provider: IAmazonReportProvider
    amazon_report_product_converter: ISalesRankReportConvertor

    def provide(self, marketplace_country: MarketplaceCountry) -> list[SalesRankProduct]:
        report_type = ReportType.SALES_RANK
        try:
            report_document = self.amazon_report_document_provider.provide(
                marketplace_country=marketplace_country,
                report_type=report_type,
                credentials=amazon_seller_credentials,
            )
        except ReportStatusError:  # Uk report not created
            logging.error('ReportStatusError: %s %s', marketplace_country, report_type)
            return []
        report_document_content = self.amazon_request_sender.get(report_document.url)
        report_document_text = report_document_content.decode('utf-8')
        save_amazon_report(
            report_document_text=report_document_text,
            marketplace_country=marketplace_country,
            report_type=report_type,
            output_file_format='csv',
        )
        return self.amazon_report_product_converter.convert(report_document_text=report_document_text,
                                                            marketplace_country=marketplace_country)

@dataclass
class SalesRankReportProductProviderFromFile(IAmazonReportDocumentProductProvider):
    amazon_report_product_converter: ISalesRankReportConvertor

    def provide(self, marketplace_country: MarketplaceCountry) -> list[SalesRankProduct]:
        report_type = ReportType.SALES_RANK
        try:
            report_document_text = read_amazon_report(
                report_type=report_type,
                marketplace_country=marketplace_country,
                file_format='csv',
            )
            return self.amazon_report_product_converter.convert(report_document_text=report_document_text,
                                                                marketplace_country=marketplace_country)
        except FileNotFoundError:
            logging.error('ReportStatusError: %s %s', marketplace_country, report_type)
            return []