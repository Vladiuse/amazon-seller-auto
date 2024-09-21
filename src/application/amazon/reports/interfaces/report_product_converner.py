from abc import ABC, abstractmethod

from src.application.amazon.reports.dto.product import AmazonInventoryReportProduct, SaleReportProduct
from src.application.amazon.common.types import MarketplaceCountry


class IReportProductConvertor(ABC):

    @abstractmethod
    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[
        AmazonInventoryReportProduct]:
        raise NotImplementedError


class ISalesReportDocumentConvertor(ABC):

    @abstractmethod
    def convert(self, report_document_text, marketplace_country: MarketplaceCountry) -> list[SaleReportProduct]:
        raise NotImplementedError
