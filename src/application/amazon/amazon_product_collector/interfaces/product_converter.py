from abc import ABC, abstractmethod

from src.application.amazon.amazon_product_collector.dto.product import AmazonProduct
from src.application.amazon.dto import Asin
from src.application.amazon.common.types import MarketplaceCountry


class IAmazonProductConvertor(ABC):

    @abstractmethod
    def convert(self, html: str, asin: Asin, marketplace_country: MarketplaceCountry) -> AmazonProduct:
        raise NotImplementedError
