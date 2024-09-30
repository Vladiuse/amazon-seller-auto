from dataclasses import dataclass

from src.application.amazon.common.types import MarketplaceCountry


class AmazonReportProduct:
    pass


@dataclass
class AmazonInventoryReportProduct(AmazonReportProduct):
    asin: str
    name: str
    marketplace_country: MarketplaceCountry
    sku: str
    available: int
    inbound: int
    featured_offer: str
    inbound_receiving_qty: int


@dataclass
class SaleReportProduct(AmazonReportProduct):
    marketplace_country: MarketplaceCountry
    asin: str
    sku: str
    units_ordered: int


@dataclass
class VendorSaleProduct(AmazonReportProduct):
    asin: str
    ordered_units: int
    marketplace_country: MarketplaceCountry


@dataclass
class FeeAmazonProduct(AmazonReportProduct):
    asin: str
    sku: str
    fba_fee: float
    marketplace_country: MarketplaceCountry


@dataclass
class ReservedProduct(AmazonReportProduct):
    asin: str
    sku: str
    marketplace_country: MarketplaceCountry
    fc_transfer: int
