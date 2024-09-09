from abc import ABC, abstractmethod

from sp_api.base import Marketplaces

from src.application.amazon_product_collector.dto.product import AmazonReportProduct


class IReportProductConvertor(ABC):

    @abstractmethod
    def convert(self, report_document_text: str, marketplace: Marketplaces) -> list[AmazonReportProduct]:
        raise NotImplementedError
