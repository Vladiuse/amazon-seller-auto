from dataclasses import dataclass

from src.application.amazon.common.types import AsinStr, MarketplaceCountry


@dataclass
class AmazonReportProduct:
    asin: AsinStr
    name: str
    marketplace_country: MarketplaceCountry
    sku: str
    available: int
    inbound: int
    featured_offer: str
    inbound_receiving_qty: int
    rating: float | None = None
    rating_reviews: int | None = None
