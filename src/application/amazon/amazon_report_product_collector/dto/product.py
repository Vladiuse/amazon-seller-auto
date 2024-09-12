from pydantic import BaseModel, ConfigDict, Field

from src.application.amazon.dto import AsinStr, MarketplaceCountry


class AmazonDocument(BaseModel):
    id: str


class AmazonReportProduct(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    asin: AsinStr
    name: str = Field(alias='product-name')
    marketplace_country: MarketplaceCountry
    sku: str
    available: int = Field(alias='afn-fulfillable-quantity')
    inbound: int = Field(alias='afn-inbound-shipped-quantity')
    featured_offer: str = Field(alias='your-price')
    inbound_receiving_qty: int = Field(alias='afn-inbound-receiving-quantity')
    rating: float | None = None
    rating_reviews: int | None = None
