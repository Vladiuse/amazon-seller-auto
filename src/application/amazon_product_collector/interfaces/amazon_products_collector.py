from abc import ABC, abstractmethod

from sp_api.base import Marketplaces, ReportType

from src.application.amazon_product_collector.dto.product import AmazonReportProduct


class IAmazonReportProductsCollector(ABC):

    @abstractmethod
    def collect(self, report_type: ReportType, marketplace: Marketplaces) -> list[AmazonReportProduct]:
        raise NotImplementedError
