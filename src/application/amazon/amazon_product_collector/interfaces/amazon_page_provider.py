from abc import ABC, abstractmethod
from src.application.amazon.dto import Asin
from src.application.amazon.common.types import MarketplaceCountry


class IAmazonProductPageProvider(ABC):

    @abstractmethod
    def provide(self, asin: Asin, marketplace_country: MarketplaceCountry) -> str:
        raise NotImplementedError
