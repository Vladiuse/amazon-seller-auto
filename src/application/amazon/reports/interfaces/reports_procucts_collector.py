from abc import ABC, abstractmethod

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.reports.dto.product import AmazonReportProduct
from src.application.amazon.reports.interfaces.report_document_product_provider import (
    IAmazonReportDocumentProductProvider,
)


class IAmazonReportsProductsCollector(ABC):
    amazon_report_document_product_provider: IAmazonReportDocumentProductProvider

    @abstractmethod
    def collects(self, marketplace_countries: list[MarketplaceCountry]) -> list[AmazonReportProduct]:
        raise NotImplementedError
