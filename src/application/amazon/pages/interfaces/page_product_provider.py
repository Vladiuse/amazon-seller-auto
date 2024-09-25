from abc import ABC, abstractmethod

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.pages.dto.product import AmazonPageProduct


class IAmazonProductProvider(ABC):

    @abstractmethod
    def collect(self, asin: str, marketplace_country: MarketplaceCountry) -> AmazonPageProduct:
        raise NotImplementedError
