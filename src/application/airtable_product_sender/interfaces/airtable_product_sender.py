import requests as req

from src.application.airtable_product_sender.dto.product_table import CREATE_AMAZON_PRODUCT_TABLE_DATA
from src.application.amazon_product_collector.dto.product import AmazonReportProduct
from src.main.config import airtable_config
import json
from pprint import pprint
from pyairtable import Api

airtable = Api(api_key=airtable_config.AIRTABLE_API_KEY)

class AirTableProductSender:

    def create_table(self):
        data = CREATE_AMAZON_PRODUCT_TABLE_DATA.model_dump_json(exclude_none=True)
        print(data)
        BASE_ID = airtable_config.AIRTABLE_APP_ID
        headers = {
            'Authorization': f'Bearer {airtable_config.AIRTABLE_API_KEY}',
            'Content-Type': 'application/json',
        }
        url = f'https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables'
        res = req.post(url, headers=headers, data=data)
        print(res.json())
        print(res.status_code)

    def send_products(self, table_id: str, products: list[AmazonReportProduct]):
        data = [product.model_dump(exclude_none=True) for product in products]


        table = airtable.table(base_id=airtable_config.AIRTABLE_APP_ID,table_name=table_id)
        pprint(table.batch_create(data))
        # url = f'https://api.airtable.com/v0/{airtable_config.AIRTABLE_APP_ID}/{table_id}'
        # print(url)
        # headers = {
        #     'Authorization': f'Bearer {airtable_config.AIRTABLE_API_KEY}',
        #     'Content-Type': 'application/json',
        # }
        # pprint(data)
        # data = json.dumps(data)
        # res = req.post(url, headers=headers, data=data)
        # print(res.json())
        # print(res.status_code)

    def _prepare_request(self, products: list[AmazonReportProduct]) -> dict:
        records = []
        for product in products:
            records.append({
                'fields': product.model_dump(exclude_none=True),
            })
        return {
            'records': records,
        }
