from pydantic import BaseModel

from src.application.amazon.common.types import MarketplaceCountry


class AmazonProductRecord(BaseModel):
    asin: str
    sku: str
    marketplace_country: MarketplaceCountry
    name: str | None = None
    available: int | None = None
    inbound: int | None = None
    featured_offer: str | None = None
    inbound_receiving_qty: int | None = None
    rating: float | None = None
    rating_reviews: int | None = None
    units_ordered: int | None = None
    fba_fee: float | None = None
    fc_transfer: int | None = None


class VendorSalesRecord(BaseModel):
    asin: str
    ordered_units: int
    marketplace_country: MarketplaceCountry
