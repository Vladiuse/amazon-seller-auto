import gzip
from dataclasses import dataclass
import os

from src.main.config import REPORTS_DIR
from src.adapters.amazon.reports.report_document_product_converter import (
    InventoryReportDocumentConverter,
    SalesReportDocumentConvertor,
)
from src.application.amazon.reports.dto.product import (
    AmazonInventoryReportProduct,
    SaleReportProduct,
)
from src.application.amazon.reports.interfaces.report_documents_provider import IAmazonReportProvider
from src.application.amazon.reports.interfaces.report_document_product_provider import (
    IAmazonReportDocumentProductProvider,
)
from src.application.amazon.reports.types import ReportType
from src.application.amazon.common.interfaces.amazon_request_sender import (
    IAmazonRequestSender,
)
from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.utils import save_amazon_report


@dataclass
class AmazonInventoryReportDocumentProductProvider(IAmazonReportDocumentProductProvider):
    amazon_request_sender: IAmazonRequestSender
    amazon_report_document_provider: IAmazonReportProvider

    def provide(self, marketplace_country: MarketplaceCountry) -> list[AmazonInventoryReportProduct]:
        report_type = ReportType.INVENTORY
        report_document = self.amazon_report_document_provider.provide(
            report_type=report_type,
            try_get_exists_report=True,
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

    def __init__(self, *args,**kwargs):
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
            report_type=report_type,
            reportOptions={"dateGranularity": "MONTH", "asinGranularity": "SKU"},
        )
        report_document_content = self.amazon_request_sender.get(report_document.url)
        report_document_text = gzip.decompress(report_document_content).decode('utf-8')
        print('text len', len(report_document_text))
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

    def __init__(self, *args,**kwargs):
        pass

    def provide(self, marketplace_country: MarketplaceCountry) -> list[SaleReportProduct]:
        report_file_name = f'{marketplace_country.value}_{ReportType.SALES.value.value}.csv'
        report_path = os.path.join(REPORTS_DIR, report_file_name)
        with open(report_path) as file:
            report_document_text = file.read()
        sales_report_converter = SalesReportDocumentConvertor()
        return sales_report_converter.convert(report_document_text=report_document_text,
                                              marketplace_country=marketplace_country)
