import os
from dataclasses import dataclass

from src.application.amazon.amazon_product_collector.interfaces.amazon_page_provider import IAmazonProductPageProvider
from src.application.amazon.common.interfaces.amazon_request_sender import IAmazonRequestSender
from src.application.amazon.common.types import Asin, MarketplaceCountry
from src.application.amazon.utils import get_marketplace_url
from src.main.config import AMAZON_PRODUCT_PAGES_DIR
from src.main.exceptions import MaxTriesError


@dataclass
class AmazonProductPageProvider(IAmazonProductPageProvider):
    amazon_request_sender: IAmazonRequestSender

    def provide(self, asin: Asin, marketplace_country: MarketplaceCountry) -> str:
        marketplace_url = get_marketplace_url(marketplace_country)
        product_url = f'{marketplace_url}dp/{asin.value}'
        return self.amazon_request_sender.get(url=product_url)


class AmazonProductPageFileReader(IAmazonProductPageProvider):

    def provide(self, asin: Asin, marketplace_country: MarketplaceCountry) -> str:
        try:
            return self.__read_amazon_product_page_file(asin=asin, marketplace_country=marketplace_country)
        except FileExistsError:
            raise MaxTriesError('provide')

    def __read_amazon_product_page_file(self, asin: Asin, marketplace_country: MarketplaceCountry) -> str:
        file_path = os.path.join(AMAZON_PRODUCT_PAGES_DIR,
                                 f'{marketplace_country.value}_{asin.value}.html')
        if not os.path.exists(file_path):
            raise FileExistsError
        with open(file_path) as file:
            return file.read()
