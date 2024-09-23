from abc import ABC, abstractmethod

from src.application.amazon.common.types import Asin, MarketplaceCountry
from src.application.amazon.pages.dto.product import AmazonPageProduct


class IAmazonProductProvider(ABC):

    @abstractmethod
    def collect(self, asin: Asin, marketplace_country: MarketplaceCountry) -> AmazonPageProduct:
        raise NotImplementedError
