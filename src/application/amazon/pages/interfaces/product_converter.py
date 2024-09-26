from abc import ABC, abstractmethod

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.pages.dto.product import AmazonPageProduct


class IAmazonProductConverter(ABC):

    @abstractmethod
    def convert(self, html: str, asin: str, marketplace_country: MarketplaceCountry) -> AmazonPageProduct:
        raise NotImplementedError
