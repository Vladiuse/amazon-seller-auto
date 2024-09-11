from abc import ABC, abstractmethod

from src.application.amazon_product_collector.dto.product import AmazonProduct

class IAmazonProductConvertor(ABC):

    @abstractmethod
    def convert(self, html: str) -> AmazonProduct:
        raise NotImplementedError