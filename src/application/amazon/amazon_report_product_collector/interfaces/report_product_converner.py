from abc import ABC, abstractmethod

from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct
from src.application.amazon.dto import MarketplaceCountry


class IReportProductConvertor(ABC):

    @abstractmethod
    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[AmazonReportProduct]:
        raise NotImplementedError
