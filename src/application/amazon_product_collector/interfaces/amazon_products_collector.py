from abc import ABC, abstractmethod
from src.application.amazon_product_collector.dto.product import AmazonProduct



class IAmazonReportProductsCollector(ABC):

    @abstractmethod
    def collect(self, report_path: str) -> list[AmazonProduct]:
        raise NotImplementedError