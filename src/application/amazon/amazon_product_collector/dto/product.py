from dataclasses import dataclass


@dataclass(frozen=True)
class AmazonProduct:
    asin: str
    marketplace_country: str
    rating: float
    reviews_total: int
