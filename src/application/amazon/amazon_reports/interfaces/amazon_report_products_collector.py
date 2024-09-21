from abc import ABC, abstractmethod

from sp_api.base import Marketplaces, ReportType

from src.application.amazon.amazon_reports.dto.product import AmazonInventoryReportProduct


class IAmazonReportProductsCollector(ABC):

    @abstractmethod
    def collect(self, report_type: ReportType, marketplace: Marketplaces) -> list[AmazonInventoryReportProduct]:
        raise NotImplementedError
