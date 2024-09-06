from abc import ABC, abstractmethod

from src.application.amazon_product_collector.dto.product import AmazonReportProduct


class IReportProductConvertor(ABC):

    @abstractmethod
    def convert(self, report_path: str) -> list[AmazonReportProduct]:
        raise NotImplementedError
