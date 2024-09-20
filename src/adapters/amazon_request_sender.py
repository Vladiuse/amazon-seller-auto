import logging

import requests
from requests.exceptions import HTTPError
from zenrows import ZenRowsClient

from src.application.amazon.common.interfaces.amazon_request_sender import IAmazonRequestSender
from src.application.amazon.utils import retry
from src.main.config import config


class AmazonZenRowsRequestSender(IAmazonRequestSender):

    @retry(
        attempts=3,
        delay=10,
        exceptions=(HTTPError,),
    )
    def get(self, url: str) -> str:
        client = ZenRowsClient(config.zenrows_config.ZENROWS_API_KEY)
        response = client.get(url)
        logging.info('Url: %s\nresponse status_code: %s', url, response.status_code)
        response.raise_for_status()
        return response.text


class AmazonRequestsRequestSender(IAmazonRequestSender):

    @retry(
        attempts=3,
        delay=10,
        exceptions=(HTTPError,),
    )
    def get(self, url: str) -> requests.Response:
        response = requests.get(url)
        logging.info('Url: %s\nresponse status_code: %s', url, response.status_code)
        response.raise_for_status()
        return response
