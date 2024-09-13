
import requests as req
from pyairtable import Api

from src.application.airtable_product_sender.dto.product_table import (
    CREATE_AMAZON_PRODUCT_TABLE_DATA,
    AmazonProductTable,
)
from src.application.airtable_product_sender.interfaces.airtable_product_sender import IAirTableProductSender
from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct
from src.main.amazonconfig import airtable_config

airtable = Api(api_key=airtable_config.AIRTABLE_API_KEY)


class AirTableProductSender(IAirTableProductSender):

    def create_table(self) -> None:
        data = CREATE_AMAZON_PRODUCT_TABLE_DATA.model_dump_json(exclude_none=True)
        headers = {
            'Authorization': f'Bearer {airtable_config.AIRTABLE_API_KEY}',
            'Content-Type': 'application/json',
        }
        url = f'https://api.airtable.com/v0/meta/bases/{airtable_config.AIRTABLE_APP_ID}/tables'
        req.post(url, headers=headers, data=data)


    def send_products_to_table(self, products: list[AmazonReportProduct]) -> None:
        products_to_send = []
        for product in products:
            data = product.model_dump(exclude_none=True)
            data['marketplace_country'] = str(data['marketplace_country'])
            product_to_send = AmazonProductTable(**data)
            products_to_send.append(product_to_send)
        AmazonProductTable.batch_save(products_to_send)
