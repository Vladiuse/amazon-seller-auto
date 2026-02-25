import logging

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.pages.dto.product import AmazonPageProduct
from src.application.amazon.pages.interfaces.page_product_provider import IAmazonProductProvider
from src.application.amazon.pages.interfaces.product_collector import IAmazonProductsCollector
from src.main.exceptions import MaxTriesError, ParserError


class AmazonProductsCollector(IAmazonProductsCollector):

    def __init__(self, product_provider: IAmazonProductProvider):
        self._product_provider = product_provider

    def collect(self, items: list[tuple[str, MarketplaceCountry]]) -> list[AmazonPageProduct]:
        products = []
        products_errors = 0
        for asin, marketplace_country in items:
            try:
                product = self._product_provider.collect(asin=asin, marketplace_country=marketplace_country)
                products.append(product)
            except (ParserError, MaxTriesError, ) as e:
                logging.error(str(e))
                products_errors += 1
        logging.error('Cant get products pages: %s', products_errors)
        return products
