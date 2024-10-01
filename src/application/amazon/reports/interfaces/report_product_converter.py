from abc import ABC, abstractmethod

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.reports.dto.product import (
    AmazonInventoryReportProduct,
    FeeAmazonProduct,
    ReservedProduct,
    SaleReportProduct,
    SalesRankProduct,
    VendorSaleProduct,
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


class IReservedReportConverter(ABC):

    @abstractmethod
    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[ReservedProduct]:
        raise NotImplementedError


class ISalesRankReportConverter(ABC):
    @abstractmethod
    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[SalesRankProduct]:
        raise NotImplementedError
