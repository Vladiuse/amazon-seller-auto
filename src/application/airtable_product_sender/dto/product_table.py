from pydantic import BaseModel

from src.application.airtable_product_sender.types import AirTableField
from src.application.amazon.common.types import MarketplaceCountry


class AirTableCreateRequest(BaseModel):
    name: str
    description: str | None = None
    fields: list[AirTableField]


class MainTableProduct(BaseModel):
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






