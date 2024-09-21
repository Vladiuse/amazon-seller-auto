from abc import ABC, abstractmethod

from src.application.amazon.reports.dto.product import AmazonReportProduct
from src.application.amazon.common.types import MarketplaceCountry


class IAmazonReportDocumentProductProvider(ABC):

    @abstractmethod
    def provide(self, marketplace_country: MarketplaceCountry) -> list[AmazonReportProduct]:
        raise NotImplementedError
