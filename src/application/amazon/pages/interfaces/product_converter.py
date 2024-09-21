from abc import ABC, abstractmethod

from src.application.amazon.pages.dto.product import AmazonProduct
from src.application.amazon.common.types import Asin, MarketplaceCountry


class IAmazonProductConvertor(ABC):

    @abstractmethod
    def convert(self, html: str, asin: Asin, marketplace_country: MarketplaceCountry) -> AmazonProduct:
        raise NotImplementedError
