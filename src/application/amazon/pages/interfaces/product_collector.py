from abc import ABC, abstractmethod

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.pages.dto.product import AmazonPageProduct


class IAmazonProductsCollector(ABC):

    @abstractmethod
    def collect(self, items: list[tuple[str, MarketplaceCountry]]) -> list[AmazonPageProduct]:
        raise NotImplementedError
