from abc import ABC, abstractmethod

from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct, SaleReportProduct
from src.application.amazon.common.types import MarketplaceCountry



class IRequestContentConverter(ABC):

    def convert(self,content:bytes) -> str:
        raise NotImplementedError


class IReportProductConvertor(ABC):

    @abstractmethod
    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[AmazonReportProduct]:
        raise NotImplementedError


class ISalesReportDocumentConvertor(ABC):

    @abstractmethod
    def convert(self, report_document_text, marketplace_country: MarketplaceCountry) -> list[SaleReportProduct]:
        raise NotImplementedError
