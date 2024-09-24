from src.adapters.airtable.tables.models import AmazonProductTable, AmazonVendorSalesTable
from src.application.airtable_product_sender.dto.product_table import AirTableCreateRequest, MainTableProduct
from src.application.airtable_product_sender.interfaces.airtable_product_sender import IAirTableProductSender
from src.application.airtable_product_sender.interfaces.airtable_table_creator import IAirtableTableCreator
from src.application.airtable_product_sender.types import AirTableField, AirTableFieldType
from src.adapters.airtable.airtable_product_sender import AirTableProductSender
from src.application.amazon.reports.dto.product import VendorSaleProduct


class CreateAmazonProductsTableUseCase:

    def __init__(self, table_creator: IAirtableTableCreator):
        self._table_creator = table_creator

    def create_table(self) -> None:
        table_request = AirTableCreateRequest(
            name='Amazon products',
            description='created by api',
            fields=[
                AirTableField(type=AirTableFieldType.SINGLE_LINE_TEXT, name='asin'),
                AirTableField(type=AirTableFieldType.SINGLE_LINE_TEXT, name='sku'),
                AirTableField(type=AirTableFieldType.SINGLE_LINE_TEXT, name='name'),
                AirTableField(type=AirTableFieldType.SINGLE_LINE_TEXT, name='marketplace_country'),
                AirTableField(type=AirTableFieldType.NUMBER, name='available', options={'precision': 0}),
                AirTableField(type=AirTableFieldType.NUMBER, name='inbound', options={'precision': 0}),
                AirTableField(type=AirTableFieldType.SINGLE_LINE_TEXT, name='featured_offer'),
                AirTableField(type=AirTableFieldType.NUMBER, name='inbound_receiving_qty', options={'precision': 0}),
                AirTableField(type=AirTableFieldType.NUMBER, name='rating', options={'precision': 2}),
                AirTableField(type=AirTableFieldType.NUMBER, name='rating_reviews', options={'precision': 0}),
                AirTableField(type=AirTableFieldType.NUMBER, name='units_ordered', options={'precision': 0}),
            ],
        )
        self._table_creator.create_table(table_request=table_request)


class UpdateAmazonProductsTableUseCase:

    def update_table(self, products: list[MainTableProduct]) -> None:
        #clean table
        records = AmazonProductTable.all()
        AmazonProductTable.batch_delete(records)
        product_sender = AirTableProductSender()
        product_sender.send_products_to_table(products=products)


class UpdateVendorTableUseCase:

    def update_table(self, vendor_sales: list[VendorSaleProduct]) -> None:
        #clean table
        records = AmazonVendorSalesTable.all()
        AmazonVendorSalesTable.batch_delete(records)
        product_sender = AirTableProductSender()
        product_sender.send_vendor_sales_data(items=vendor_sales)



