import logging
from dataclasses import dataclass

from requests.exceptions import HTTPError
from zenrows import ZenRowsClient

from src.application.amazon.amazon_product_collector.dto.product import AmazonProduct
from src.application.amazon.amazon_product_collector.interfaces.amazon_page_provider import IAmazonProductPageProvider
from src.application.amazon.amazon_product_collector.interfaces.product_collector import IAmazonProductCollector
from src.application.amazon.amazon_product_collector.interfaces.product_converter import IAmazonProductConvertor
from src.application.amazon.dto import Asin, MarketplaceCountry
from src.application.amazon.utils import retry
from src.main.config import config


@dataclass
class AmazonProductCollector(IAmazonProductCollector):
    product_convertor: IAmazonProductConvertor
    product_page_provider: IAmazonProductPageProvider

    def collect(self, asin: Asin, marketplace_country: MarketplaceCountry) -> AmazonProduct:
        html = self.product_page_provider.provide(asin=asin, marketplace_country=marketplace_country)
        return self.product_convertor.convert(html=html, asin=asin, marketplace_country=marketplace_country)

    @retry(
        attempts=5,
        delay=5,
        exceptions=(HTTPError,),
    )
    def get_amazon_product_page(self, asin: Asin, marketplace_country: MarketplaceCountry) -> str:
        client = ZenRowsClient(config.zenrows_config.ZENROWS_API_KEY)
        url = f'{marketplace_country.url}dp/{asin.value}'
        response = client.get(url)
        logging.info('%s\nresponse status_code: %s', url, response.status_code)
        response.raise_for_status()
        return response.text
