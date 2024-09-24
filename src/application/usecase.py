import logging

from src.adapters.airtable.airtable_product_sender import AirTableProductSender
from src.adapters.airtable.tables_records_builders import MainTableObjectsBuilder, VendorSalesObjectsBuilder
from src.adapters.amazon.pages.page_provider import AmazonProductPageFileReader
from src.adapters.amazon.pages.product_collector import AmazonProductProvider
from src.adapters.amazon.pages.product_converter import AmazonProductConverter
from src.adapters.amazon.reports.report import AmazonReportCreator, AmazonReportDocumentGetter, AmazonReportGetter
from src.adapters.amazon.reports.report_document_product_provider import (
    InventoryReportProviderFromFile,
    SalesReportProviderFromFile,
    VendorSalesReportProviderFromFile,
)
from src.adapters.amazon.reports.report_documents_provider import AmazonReportDocumentProvider
from src.adapters.amazon.reports.reports_procucts_collector import AmazonReportsProductsCollector
from src.adapters.amazon_request_sender import AmazonRequestsRequestSender, AmazonZenRowsRequestSender
from src.application.airtable_product_sender.usecase import UpdateAmazonProductsTableUseCase, UpdateVendorTableUseCase
from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.pages.usecase import AmazonProductsCollector
from src.application.amazon.utils import get_active_asins
from src.main.config import AMAZON_PRODUCT_PAGES_DIR


class CollectProductsAndSendToAirtableUseCase:

    def collect_and_send(self, marketplace_countries: list[MarketplaceCountry]) -> None:
        report_getter = AmazonReportGetter()
        report_creator = AmazonReportCreator()
        report_document_getter = AmazonReportDocumentGetter()
        report_document_provider = AmazonReportDocumentProvider(
            report_getter=report_getter,
            report_creator=report_creator,
            report_document_getter=report_document_getter,
        )
        amazon_request_sender = AmazonRequestsRequestSender()

        # inventory product provider
        inventory_report_document_product_provider = InventoryReportProviderFromFile(  #
            amazon_request_sender=amazon_request_sender,
            amazon_report_document_provider=report_document_provider,
        )
        # sales product provider
        sales_report_document_product_provider = SalesReportProviderFromFile(  #
            amazon_request_sender=amazon_request_sender,
            amazon_report_document_provider=report_document_provider,
        )
        inventory_collector = AmazonReportsProductsCollector(
            amazon_report_document_product_provider=inventory_report_document_product_provider,
        )
        sales_collector = AmazonReportsProductsCollector(
            amazon_report_document_product_provider=sales_report_document_product_provider,
        )
        inventory_products = inventory_collector.collects(marketplace_countries=marketplace_countries)
        sales_products = sales_collector.collects(marketplace_countries=marketplace_countries)
        logging.info('inventory_products: %s', len(inventory_products))
        logging.info('sales_products: %s', len(sales_products))

        # Load rating and reviews
        amazon_request_sender = AmazonZenRowsRequestSender()
        product_collector = AmazonProductProvider(
            product_convertor=AmazonProductConverter(),
            # product_page_provider=AmazonProductPageProvider(amazon_request_sender=amazon_request_sender),
            product_page_provider=AmazonProductPageFileReader(products_dir=AMAZON_PRODUCT_PAGES_DIR),  # TEST
        )
        product_collector = AmazonProductsCollector(
            product_collector=product_collector,
        )
        table_objects_creator = MainTableObjectsBuilder()
        table_objects_creator.add_inventory_data(items=inventory_products)
        table_objects_creator.add_sales_data(items=sales_products)
        unique_asins_geo_pairs = table_objects_creator.get_unique_asins_geo_pairs()
        logging.info('unique_asins_geo_pairs: %s', len(unique_asins_geo_pairs))
        products_from_pars = product_collector.collect(items=unique_asins_geo_pairs)
        logging.info('products_from_pars: %s', len(products_from_pars))
        table_objects_creator.add_rating_data(items=products_from_pars)
        active_asins = get_active_asins(return_string=True)

        #Send data to airtable
        products_to_send = []
        for record in table_objects_creator.items.values():
            if record.asin in active_asins:
                products_to_send.append(record)
        update_main_table_use_case = UpdateAmazonProductsTableUseCase(

        )
        update_main_table_use_case.update_table(products=products_to_send)

        # Vendor Sales
        vendor_sales_report_product_provider = VendorSalesReportProviderFromFile( #
            amazon_request_sender=amazon_request_sender,
            amazon_report_document_provider=report_document_provider,
        )
        all_vendor_sales = []
        for marketplace_country in marketplace_countries:
            products = vendor_sales_report_product_provider.provide(marketplace_country=marketplace_country)
            all_vendor_sales.extend(products)

        vendor_sales_builder = VendorSalesObjectsBuilder()
        vendor_sales_builder.add_vendor_sales_data(items=all_vendor_sales)
        logging.info('Vendor sales records count: %s', len(vendor_sales_builder.items))
        vendor_use_case = UpdateVendorTableUseCase()
        vendor_use_case.update_table(vendor_sales_records=vendor_sales_builder.items)