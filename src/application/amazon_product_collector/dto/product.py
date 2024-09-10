from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    rating: float
    reviews_total: int
