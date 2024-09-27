import logging

from src.adapters.airtable.airtable_product_sender import AirTableProductSender
from src.adapters.airtable.tables_records_builders import MainTableRecordsBuilder, VendorSalesRecordsBuilder
from src.adapters.amazon.pages.page_product_provider import AmazonProductProvider
from src.adapters.amazon.pages.page_provider import AmazonProductPageFileReader, AmazonProductPageProvider
from src.adapters.amazon.pages.product_collector import AmazonProductsCollector
from src.adapters.amazon.pages.product_converter import AmazonProductConverter
from src.adapters.amazon.reports.report import AmazonReportCreator, AmazonReportDocumentGetter, AmazonReportGetter
from src.adapters.amazon.reports.report_document_product_converter import (
    InventoryReportDocumentConverter,
    SalesReportDocumentConverter,
    VendorSalesReportConverter,
    ReservedReportConverter,
    FeeReportConverter,
)
from src.adapters.amazon.reports.report_document_product_provider import (
    AmazonInventoryReportDocumentProductProvider,
    AmazonSalesReportDocumentProductProvider,
    AmazonVendorSalesReportDocumentProductProvider,
    FeeReportDocumentProvider,
    InventoryReportProviderFromFile,
    SalesReportProviderFromFile,
    VendorSalesReportProviderFromFile,
    FeeReportProviderFromFile,
    ReservedReportProductProvider,
    ReservedReportProductProviderFromFile,
)
from src.adapters.amazon.reports.report_documents_provider import AmazonReportDocumentProvider
from src.adapters.amazon.reports.reports_procucts_collector import AmazonReportsProductsCollector
from src.adapters.amazon_request_sender import AmazonRequestsRequestSender, AmazonZenRowsRequestSender
from src.application.amazon.common.types import MarketplaceCountry
from src.application.usecase import CollectProductsAndSendToAirtableUseCase
from src.main.config import AMAZON_PRODUCT_PAGES_DIR


logging.basicConfig(level=logging.INFO)

marketplace_countries = [
    MarketplaceCountry.IT,
    MarketplaceCountry.ES,
    MarketplaceCountry.DE,
    MarketplaceCountry.FR,
    MarketplaceCountry.UK,
]

report_document_provider = AmazonReportDocumentProvider(
    report_getter=AmazonReportGetter(),
    report_creator=AmazonReportCreator(),
    report_document_getter=AmazonReportDocumentGetter(),
)
amazon_request_sender = AmazonRequestsRequestSender()
inventory_report_document_product_provider = AmazonInventoryReportDocumentProductProvider(
    # for test InventoryReportProviderFromFile, from amazon AmazonInventoryReportDocumentProductProvider
    amazon_request_sender=amazon_request_sender,
    amazon_report_document_provider=report_document_provider,
    amazon_report_product_converter=InventoryReportDocumentConverter(),
)
sales_report_document_product_provider = AmazonSalesReportDocumentProductProvider(
    # for test SalesReportProviderFromFile, from amazon AmazonSalesReportDocumentProductProvider
    amazon_request_sender=amazon_request_sender,
    amazon_report_document_provider=report_document_provider,
    amazon_report_product_converter=SalesReportDocumentConverter(),
)
vendor_sales_report_product_provider = AmazonVendorSalesReportDocumentProductProvider(
    # for test VendorSalesReportProviderFromFile, from amazon AmazonVendorSalesReportDocumentProductProvider
    amazon_request_sender=amazon_request_sender,
    amazon_report_document_provider=report_document_provider,
    amazon_report_product_converter=VendorSalesReportConverter(),
)
fee_report_product_provider = FeeReportDocumentProvider(
    # for test FeeReportProviderFromFile, from amazon FeeReportDocumentProvider
    amazon_request_sender=amazon_request_sender,
    amazon_report_document_provider=report_document_provider,
    amazon_report_product_converter=FeeReportConverter(),
)
reserved_report_product_provider = ReservedReportProductProvider(
    # for test ReservedReportProductProviderFromFile, from amazon ReservedReportProductProvider
    amazon_request_sender=amazon_request_sender,
    amazon_report_document_provider=report_document_provider,
    amazon_report_product_converter=ReservedReportConverter(),
)

inventory_collector = AmazonReportsProductsCollector(
    amazon_report_document_product_provider=inventory_report_document_product_provider,
)
sales_collector = AmazonReportsProductsCollector(
    amazon_report_document_product_provider=sales_report_document_product_provider,
)
vendor_sales_collector = AmazonReportsProductsCollector(
    amazon_report_document_product_provider=vendor_sales_report_product_provider,
)
fee_collector = AmazonReportsProductsCollector(
    amazon_report_document_product_provider=fee_report_product_provider,
)
reserved_collector = AmazonReportsProductsCollector(
    amazon_report_document_product_provider=reserved_report_product_provider,
)

product_provider = AmazonProductProvider(
    product_converter=AmazonProductConverter(),
    product_page_provider=AmazonProductPageProvider(amazon_request_sender=amazon_request_sender),
    # product_page_provider=AmazonProductPageFileReader(products_dir=AMAZON_PRODUCT_PAGES_DIR),  # TEST
)
product_collector = AmazonProductsCollector(
    product_provider=product_provider,
)
airtable_product_sender = AirTableProductSender()

amazon_products_records_builder = MainTableRecordsBuilder()
amazon_vendor_records_builder = VendorSalesRecordsBuilder()

use_case = CollectProductsAndSendToAirtableUseCase(
    inventory_collector=inventory_collector,
    sales_collector=sales_collector,
    vendor_sales_collector=vendor_sales_collector,
    fee_collector=fee_collector,
    reserved_collector=reserved_collector,
    product_collector=product_collector,
    airtable_product_sender=airtable_product_sender,
    amazon_products_records_builder=amazon_products_records_builder,
    amazon_vendor_records_builder=amazon_vendor_records_builder,
)
use_case.collect_and_send(marketplace_countries=marketplace_countries)
