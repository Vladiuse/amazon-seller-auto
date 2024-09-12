import logging

from src.application.amazon.amazon_product_collector.dto.product import AmazonProduct
from src.application.amazon.amazon_product_collector.interfaces.product_collector import IAmazonProductCollector
from src.application.amazon.dto import Asin, MarketplaceCountry
from src.main.exceptions import MaxTriesError, ParserError

logging.basicConfig(level=logging.INFO)


class CollectAmazonProductsUseCase:

    def __init__(self, product_collector: IAmazonProductCollector):
        self._product_collector = product_collector

    def collect(self, items: list[tuple[Asin, MarketplaceCountry]]) -> list[AmazonProduct]:
        products = []
        for asin, marketplace_country in items:
            try:
                product = self._product_collector.collect(asin=asin, marketplace_country=marketplace_country)
                logging.info(product)
                products.append(product)
            except (ParserError, MaxTriesError) as e:
                logging.error(e)  # TODO no error text
        return products
