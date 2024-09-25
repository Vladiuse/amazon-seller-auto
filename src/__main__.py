import logging

from src.adapters.airtable.airtable_product_sender import AirTableProductSender
from src.adapters.amazon.pages.page_product_provider import AmazonProductProvider
from src.adapters.amazon.pages.page_provider import AmazonProductPageFileReader
from src.adapters.amazon.pages.product_collector import AmazonProductsCollector
from src.adapters.amazon.pages.product_converter import AmazonProductConverter
from src.adapters.amazon.reports.report import AmazonReportCreator, AmazonReportDocumentGetter, AmazonReportGetter
from src.adapters.amazon.reports.report_document_product_converter import (
    InventoryReportDocumentConverter,
    SalesReportDocumentConvertor,
    VendorSalesReportConverter,
)
from src.adapters.amazon.reports.report_document_product_provider import (
    InventoryReportProviderFromFile,
    SalesReportProviderFromFile,
    VendorSalesReportProviderFromFile,
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
inventory_report_document_product_provider = InventoryReportProviderFromFile(  #
    # amazon_request_sender=amazon_request_sender,
    # amazon_report_document_provider=report_document_provider,
    amazon_report_product_converter=InventoryReportDocumentConverter(),
)
sales_report_document_product_provider = SalesReportProviderFromFile(  #
    # amazon_request_sender=amazon_request_sender,
    # amazon_report_document_provider=report_document_provider,
    amazon_report_product_converter=SalesReportDocumentConvertor(),
)
vendor_sales_report_product_provider = VendorSalesReportProviderFromFile(  #
    # amazon_request_sender=amazon_request_sender,
    # amazon_report_document_provider=report_document_provider,
    amazon_report_product_converter=VendorSalesReportConverter(),
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

amazon_request_sender = AmazonZenRowsRequestSender()
product_provider = AmazonProductProvider(
    product_convertor=AmazonProductConverter(),
    # product_page_provider=AmazonProductPageProvider(amazon_request_sender=amazon_request_sender),
    product_page_provider=AmazonProductPageFileReader(products_dir=AMAZON_PRODUCT_PAGES_DIR),  # TEST
)
product_collector = AmazonProductsCollector(
    product_provider=product_provider,
)
airtable_product_sender = AirTableProductSender()

use_case = CollectProductsAndSendToAirtableUseCase(
    inventory_collector=inventory_collector,
    sales_collector=sales_collector,
    vendor_sales_collector=vendor_sales_collector,
    product_collector=product_collector,
    airtable_product_sender=airtable_product_sender,
)
use_case.collect_and_send(marketplace_countries=marketplace_countries)
