import logging
from dataclasses import dataclass

from src.adapters.airtable.tables.models import AmazonProductTable, AmazonVendorSalesTable
from src.adapters.airtable.tables_records_builders import MainTableObjectsBuilder, VendorSalesObjectsBuilder
from src.application.airtable_product_sender.interfaces.airtable_product_sender import IAirTableProductSender
from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.pages.interfaces.product_collector import IAmazonProductsCollector
from src.application.amazon.reports.interfaces.reports_procucts_collector import IAmazonReportsProductsCollector
from src.application.amazon.utils import get_active_asins


@dataclass
class CollectProductsAndSendToAirtableUseCase:
    inventory_collector: IAmazonReportsProductsCollector
    sales_collector: IAmazonReportsProductsCollector
    vendor_sales_collector: IAmazonReportsProductsCollector
    product_collector: IAmazonProductsCollector
    airtable_product_sender: IAirTableProductSender

    def collect_and_send(self, marketplace_countries: list[MarketplaceCountry]) -> None:
        # Amazon Products Table
        inventory_products = self.inventory_collector.collects(marketplace_countries=marketplace_countries)
        sales_products = self.sales_collector.collects(marketplace_countries=marketplace_countries)
        logging.info('inventory_products: %s', len(inventory_products))
        logging.info('sales_products: %s', len(sales_products))
        table_objects_creator = MainTableObjectsBuilder()
        table_objects_creator.add_inventory_data(items=inventory_products)
        table_objects_creator.add_sales_data(items=sales_products)
        unique_asins_geo_pairs = table_objects_creator.get_unique_asins_geo_pairs()
        logging.info('unique_asins_geo_pairs: %s', len(unique_asins_geo_pairs))
        products_from_pars = self.product_collector.collect(items=unique_asins_geo_pairs)
        logging.info('products_from_pars: %s', len(products_from_pars))
        table_objects_creator.add_rating_data(items=products_from_pars)
        active_asins = get_active_asins()
        products_to_send = []
        for record in table_objects_creator.items.values():
            if record.asin in active_asins:
                products_to_send.append(record)
        records = AmazonProductTable.all()
        AmazonProductTable.batch_delete(records)
        self.airtable_product_sender.send_products_to_table(products=products_to_send)

        # Vendor Sales Table
        all_vendor_sales = self.vendor_sales_collector.collects(marketplace_countries=marketplace_countries)
        vendor_sales_builder = VendorSalesObjectsBuilder()
        vendor_sales_builder.add_vendor_sales_data(items=all_vendor_sales)
        logging.info('Vendor sales records count: %s', len(vendor_sales_builder.items))
        records = AmazonVendorSalesTable.all()
        AmazonVendorSalesTable.batch_delete(records)
        self.airtable_product_sender.send_vendor_sales_data(items=vendor_sales_builder.items)
