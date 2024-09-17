from src.application.airtable_product_sender.interfaces.airtable_product_sender import IAirTableProductSender
from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct

from .tables.models import AmazonProductTable


class AirTableProductSender(IAirTableProductSender):

    def send_products_to_table(self, products: list[AmazonReportProduct]) -> None:
        products_to_send = []
        for product in products:
            data = product.model_dump(exclude_none=True)
            data['marketplace_country'] = str(data['marketplace_country'])
            product_to_send = AmazonProductTable(**data)
            products_to_send.append(product_to_send)
        AmazonProductTable.batch_save(products_to_send)
