from src.application.airtable_product_sender.dto.product_table import MainTableProduct
from src.application.airtable_product_sender.interfaces.airtable_product_sender import IAirTableProductSender
from src.application.amazon.reports.dto.product import VendorSaleProduct
from .tables.models import AmazonProductTable, AmazonVendorSalesTable


class AirTableProductSender(IAirTableProductSender):

    def send_products_to_table(self, products: list[MainTableProduct]) -> None:
        products_to_send = []
        for product in products:
            product_to_send = AmazonProductTable(
                asin=product.asin,
                sku=product.sku,
                name=product.name,
                marketplace_country=product.marketplace_country.value,
                available=product.available,
                inbound=product.inbound,
                featured_offer=product.featured_offer,
                inbound_receiving_qty=product.inbound_receiving_qty,
                rating=product.rating,
                rating_reviews=product.rating_reviews,
                units_ordered=product.units_ordered,
            )
            products_to_send.append(product_to_send)
        AmazonProductTable.batch_save(products_to_send)

    def send_vendor_sales_data(self, items: list[VendorSaleProduct]) -> None:
        vendor_sales_to_sand = []
        for item in items:
            vendor_record = AmazonVendorSalesTable(
                asin=item.asin,
                marketplace_country=item.marketplace_country.value,
                ordered_units=item.ordered_units,
            )
            vendor_sales_to_sand.append(vendor_record)
        AmazonVendorSalesTable.batch_save(vendor_sales_to_sand)




