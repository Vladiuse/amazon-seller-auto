import requests

from src.application.airtable_product_sender.dto.product_table import AirTableRequest
from src.application.airtable_product_sender.interfaces.airtable_table_creator import IAirtableTableCreator
from src.main.config import config


class AirtableTableCreator(IAirtableTableCreator):

    def create_table(self, table_request: AirTableRequest) -> None:
        headers = {
            'Authorization': f'Bearer {config.airtable_config.AIRTABLE_API_KEY}',
            'Content-Type': 'application/json',
        }
        url = f'https://api.airtable.com/v0/meta/bases/{config.airtable_config.AIRTABLE_APP_ID}/tables'
        table_data = table_request.model_dump_json(exclude_none=True)
        requests.post(url, headers=headers, data=table_data)
