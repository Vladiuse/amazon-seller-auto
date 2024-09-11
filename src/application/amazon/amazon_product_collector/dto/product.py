from dataclasses import dataclass


@dataclass(frozen=True)
class AmazonProduct:
    rating: float
    reviews_total: int
