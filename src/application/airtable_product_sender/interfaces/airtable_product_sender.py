import json
import logging
from pprint import pprint

import requests as req
from pyairtable import Api

from src.application.airtable_product_sender.dto.product_table import (
    CREATE_AMAZON_PRODUCT_TABLE_DATA,
    AmazonProductTable,
)
from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct
from src.main.config import airtable_config

airtable = Api(api_key=airtable_config.AIRTABLE_API_KEY)


class AirTableProductSender:

    def create_table(self) -> None:
        data = CREATE_AMAZON_PRODUCT_TABLE_DATA.model_dump_json(exclude_none=True)
        BASE_ID = airtable_config.AIRTABLE_APP_ID
        headers = {
            'Authorization': f'Bearer {airtable_config.AIRTABLE_API_KEY}',
            'Content-Type': 'application/json',
        }
        url = f'https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables'
        req.post(url, headers=headers, data=data)

    def send_products(self, table_id: str, products: list[AmazonReportProduct]):
        data = [product.model_dump(exclude_none=True) for product in products]
        table = airtable.table(base_id=airtable_config.AIRTABLE_APP_ID, table_name=table_id)
        table.batch_create(data)

        url = f'https://api.airtable.com/v0/{airtable_config.AIRTABLE_APP_ID}/{table_id}'
        headers = {
            'Authorization': f'Bearer {airtable_config.AIRTABLE_API_KEY}',
            'Content-Type': 'application/json',
        }
        pprint(data)
        data = json.dumps(data)
        res = req.post(url, headers=headers, data=data)
        print(res.json())
        print(res.status_code)

    def clean_table(self) -> None:
        records = AmazonProductTable.all()
        AmazonProductTable.batch_delete(records)

    def send_products_to_table(self, products: list[AmazonReportProduct]) -> None:
        products_to_send = []
        for product in products:
            data = product.model_dump(exclude_none=True)
            data['marketplace_country'] = str(data['marketplace_country'])
            product_to_send = AmazonProductTable(**data)
            products_to_send.append(product_to_send)
        res = AmazonProductTable.batch_save(products_to_send)
        logging.info(res)

    def _prepare_request(self, products: list[AmazonReportProduct]) -> dict:
        records = []
        for product in products:
            records.append({
                'fields': product.model_dump(exclude_none=True),
            })
        return {
            'records': records,
        }
