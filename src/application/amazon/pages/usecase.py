import logging

from src.application.amazon.pages.dto.product import AmazonPageProduct
from src.application.amazon.pages.interfaces.product_collector import IAmazonProductProvider
from src.application.amazon.common.types import Asin, MarketplaceCountry
from src.main.exceptions import MaxTriesError, ParserError


class AmazonProductsCollector:

    def __init__(self, product_collector: IAmazonProductProvider):
        self._product_collector = product_collector

    def collect(self, items: list[tuple[Asin, MarketplaceCountry]]) -> list[AmazonPageProduct]:
        products = []
        products_errors = 0
        for asin, marketplace_country in items:
            try:
                product = self._product_collector.collect(asin=asin, marketplace_country=marketplace_country)
                products.append(product)
            except (ParserError, MaxTriesError) as e:
                logging.error(str(e))
                products_errors += 1
        logging.error('Cant get products pages: %s', products_errors)
        return products
