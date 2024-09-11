from abc import ABC, abstractmethod

from src.application.amazon.amazon_product_collector import AmazonProduct

class IAmazonProductConvertor(ABC):

    @abstractmethod
    def convert(self, html: str) -> AmazonProduct:
        raise NotImplementedError