from abc import ABC, abstractmethod

from sp_api.base import ReportType

from src.application.amazon.amazon_report_product_collector.dto.report import AmazonReportProduct


class IAmazonReportCreator(ABC):

    @abstractmethod
    def create_report(self, report_type: ReportType) -> str:
        raise NotImplementedError


class IAmazonReport(ABC):

    @abstractmethod
    def get_report(self, report_id: str) -> AmazonReportProduct:
        raise NotImplementedError
