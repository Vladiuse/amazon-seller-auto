from dataclasses import dataclass

from src.application.amazon.common.types import MarketplaceCountry


@dataclass(frozen=True)
class AmazonPageProduct:
    asin: str
    marketplace_country: MarketplaceCountry
    rating: float
    rating_reviews: int
