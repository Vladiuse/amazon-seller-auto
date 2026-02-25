from abc import ABC, abstractmethod

from src.application.amazon.common.types import MarketplaceCountry


class IAmazonProductPageProvider(ABC):

    @abstractmethod
    def provide(self, asin: str, marketplace_country: MarketplaceCountry) -> str:
        raise NotImplementedError
