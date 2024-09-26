from abc import ABC, abstractmethod

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.reports.dto.product import (
    AmazonInventoryReportProduct,
    SaleReportProduct,
    VendorSaleProduct,
    FeeAmazonProduct,
)


class IInventoryReportConverter(ABC):

    @abstractmethod
    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[
        AmazonInventoryReportProduct]:
        raise NotImplementedError


class ISalesReportConverter(ABC):

    @abstractmethod
    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[SaleReportProduct]:
        raise NotImplementedError


class IVendorSalesReportConverter(ABC):

    @abstractmethod
    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[VendorSaleProduct]:
        raise NotImplementedError


class IFeeReportConverter(ABC):

    @abstractmethod
    def convert(self, report_document_text: str) -> list[FeeAmazonProduct]:
        raise NotImplementedError
