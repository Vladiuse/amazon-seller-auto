from abc import ABC, abstractmethod

from src.application.amazon.pages.dto.product import AmazonProduct
from src.application.amazon.common.types import Asin, MarketplaceCountry


class IAmazonProductCollector(ABC):

    @abstractmethod
    def collect(self, asin: Asin, marketplace_country: MarketplaceCountry) -> AmazonProduct:
        raise NotImplementedError
