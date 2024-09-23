import logging

from src.adapters.airtable.airtable_product_sender import AirTableProductSender
from src.adapters.airtable.maintable_manager import MainTableObjectsManager
from src.adapters.amazon.pages.page_provider import AmazonProductPageFileReader
from src.adapters.amazon.pages.product_collector import AmazonProductProvider
from src.adapters.amazon.pages.product_converter import AmazonProductConverter
from src.adapters.amazon.reports.report import AmazonReportCreator, AmazonReportDocumentGetter, AmazonReportGetter
from src.adapters.amazon.reports.report_document_product_provider import (
    InventoryReportProviderFromFile,
    SalesReportProviderFromFile,
)
from src.adapters.amazon.reports.report_documents_provider import AmazonReportDocumentProvider
from src.adapters.amazon.reports.reports_procucts_collector import AmazonReportsProductsCollector
from src.adapters.amazon_request_sender import AmazonRequestsRequestSender, AmazonZenRowsRequestSender
from src.application.airtable_product_sender.usecase import UpdateAmazonProductsTableUseCase
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
        manager = MainTableObjectsManager()
        manager.add_inventory_data(items=inventory_products)
        manager.add_sales_data(items=sales_products)
        unique_asins_geo_pairs = manager.get_unique_asins_geo_pairs()
        logging.info('unique_asins_geo_pairs: %s', len(unique_asins_geo_pairs))
        products_from_pars = product_collector.collect(items=unique_asins_geo_pairs)
        logging.info('products_from_pars: %s', len(products_from_pars))
        manager.add_rating_data(items=products_from_pars)
        active_asins = get_active_asins(return_string=True)

        #Send data to airtable
        products_to_send = []
        for record in manager.items.values():
            if record.asin in active_asins:
                products_to_send.append(record)
        update_products_use_case = UpdateAmazonProductsTableUseCase(
            product_sender=AirTableProductSender(),
        )
        update_products_use_case.update_table(products=products_to_send)