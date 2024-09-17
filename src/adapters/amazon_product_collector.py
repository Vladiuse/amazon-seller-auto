import logging
import os
from dataclasses import dataclass

from requests.exceptions import HTTPError
from zenrows import ZenRowsClient

from src.adapters.amazon_product_converter import AmazonProductConverter
from src.application.amazon.amazon_product_collector.dto.product import AmazonProduct
from src.application.amazon.amazon_product_collector.interfaces.product_collector import IAmazonProductCollector
from src.application.amazon.dto import Asin, MarketplaceCountry
from src.application.amazon.utils import retry
from src.main.config import AMAZON_PRODUCT_PAGES_DIR, config
from src.main.exceptions import MaxTriesError


@dataclass
class AmazonProductCollector(IAmazonProductCollector):
    product_convertor: AmazonProductConverter

    def collect(self, asin: Asin, marketplace_country: MarketplaceCountry) -> AmazonProduct:
        html = self.get_amazon_product_page(asin=asin, marketplace_country=marketplace_country)
        return self.product_convertor.convert(html=html, asin=asin, marketplace_country=marketplace_country)

    @retry(
        attempts=5,
        delay=5,
        exceptions=(HTTPError, ),
    )
    def get_amazon_product_page(self, asin: Asin, marketplace_country: MarketplaceCountry) -> str:
        client = ZenRowsClient(config.zenrows_config.ZENROWS_API_KEY)
        url = f'{marketplace_country.url}dp/{asin.value}'
        res = client.get(url)
        logging.info(url)
        logging.info('response status code: %s', res.status_code)
        res.raise_for_status()
        html = res.text
        self.__write_html_in_file(asin=asin, marketplace_country=marketplace_country, html=html)
        return html

    def __write_html_in_file(self, asin: Asin, marketplace_country: MarketplaceCountry, html: str) -> None:
        file_name = f'{marketplace_country.country_code}_{asin.value}.html'
        file_path = os.path.join(AMAZON_PRODUCT_PAGES_DIR, file_name)
        with open(file_path, 'w') as file:
            file.write(html)


class AmazonProductCollectorFromSavedFile(AmazonProductCollector):

    def get_amazon_product_page(self, asin: Asin, marketplace_country: MarketplaceCountry) -> str:
        file_name = f'{marketplace_country.country_code}_{asin.value}.html'
        file_path = os.path.join(AMAZON_PRODUCT_PAGES_DIR, file_name)
        if os.path.exists(file_path):
            with open(file_path) as file:
                return file.read()
        raise MaxTriesError
