import os

from src.application.amazon.amazon_product_collector.interfaces.amazon_page_provider import IAmazonProductPageProvider
from src.application.amazon.dto import Asin, MarketplaceCountry
from src.main.config import AMAZON_PRODUCT_PAGES_DIR
from src.main.exceptions import MaxTriesError


class AmazonProductPageProvider(IAmazonProductPageProvider):

    def __init__(self, request_sender):
        self._request_sender = request_sender

    def provide(self, asin: Asin, marketplace_country: MarketplaceCountry) -> str:
        url = f'{marketplace_country.url}dp/{asin.value}'
        return self._request_sender(url=url)


class AmazonProductPageProviderFromFile(IAmazonProductPageProvider):

    def provide(self, asin: Asin, marketplace_country: MarketplaceCountry) -> str:
        try:
            return self.__get_amazon_product_page_from_file(asin=asin, marketplace_country=marketplace_country)
        except FileExistsError:
            raise MaxTriesError

    def __get_amazon_product_page_from_file(self, asin: Asin, marketplace_country: MarketplaceCountry) -> str:
        file_path = os.path.join(AMAZON_PRODUCT_PAGES_DIR,
                                 f'{marketplace_country.country_code}_{asin.value}.html')
        if not os.path.exists(file_path):
            raise FileExistsError
        with open(file_path) as file:
            return file.read()
