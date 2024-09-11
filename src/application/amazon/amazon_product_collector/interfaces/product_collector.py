from abc import ABC, abstractmethod

from src.application.amazon.amazon_product_collector.dto.product import AmazonProduct
from src.application.amazon.dto import Asin, MarketplaceCountry


class IAmazonProductCollector(ABC):

    @abstractmethod
    def collect(self, asin: Asin, marketplace_country: MarketplaceCountry) -> AmazonProduct:
        raise NotImplementedError
