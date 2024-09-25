from abc import ABC, abstractmethod

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.reports.dto.product import (
    AmazonInventoryReportProduct,
    SaleReportProduct,
    VendorSaleProduct,
)


class IInventoryReportConvertor(ABC):

    @abstractmethod
    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[
        AmazonInventoryReportProduct]:
        raise NotImplementedError


class ISalesReportConvertor(ABC):

    @abstractmethod
    def convert(self, report_document_text, marketplace_country: MarketplaceCountry) -> list[SaleReportProduct]:
        raise NotImplementedError


class IVendorSalesReportConverter(ABC):

    @abstractmethod
    def convert(self, report_document_text, marketplace_country: MarketplaceCountry) -> list[VendorSaleProduct]:
        raise NotImplementedError
