from enum import Enum

from pydantic import BaseModel, Field, ConfigDict
from sp_api.base import Marketplaces, ReportType
from src.application.amazon.dto import AsinStr




class AmazonDocument(BaseModel):
    id: str


class AmazonReport(BaseModel):
    id:str|None = None
    marketplace: Marketplaces
    type:ReportType
    document: AmazonDocument


class MarketplaceCountry(str, Enum):
    FR = 'FR'
    IT = 'IT'
    DE = 'DE'
    GB = 'GB'
    UK = 'UK'
    ES = 'ES'

# https://www.amazon.co.uk/
# https://www.amazon.de/
# https://www.amazon.es/
# https://www.amazon.fr
# https://www.amazon.it/


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



