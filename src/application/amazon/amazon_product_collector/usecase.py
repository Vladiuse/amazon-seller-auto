import logging

from src.adapters.amazon_product_collector import AmazonProductCollector
from src.adapters.amazon_product_convertor import AmazonProductConvertor
from src.application.amazon.amazon_product_collector.dto.product import AmazonProduct
from src.application.amazon.dto import Asin, MarketplaceCountry

logging.basicConfig(level=logging.INFO)


class CollectAmazonProductsUseCase:

    def collect(self, items: list[tuple[Asin, MarketplaceCountry]]) -> list[AmazonProduct]:
        collector = AmazonProductCollector(
            product_convertor=AmazonProductConvertor(),
        )
        products = []
        for asin, marketplace_country in items:
            print(asin, marketplace_country)
            try:
                product = collector.collect(asin=asin, marketplace_country=marketplace)
                products.append(product)
            except (ParserError, MaxTriesError) as e:
                logging.error(e)
        return products
