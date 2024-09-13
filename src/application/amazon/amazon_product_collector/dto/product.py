from dataclasses import dataclass

from src.application.amazon.dto import Asin, MarketplaceCountry


@dataclass(frozen=True)
class AmazonProduct:
    asin: Asin
    marketplace_country: MarketplaceCountry
    rating: float
    rating_reviews: int
