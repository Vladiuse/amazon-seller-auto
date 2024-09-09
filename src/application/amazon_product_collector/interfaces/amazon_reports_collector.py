from abc import ABC, abstractmethod

from sp_api.base import ReportType

from src.application.amazon_product_collector.dto.report import AmazonReport, ReportDocument


class IAmazonReportCollector(ABC):

    @abstractmethod
    def create_report(self, report_type: ReportType) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_report(self, report_id: str) -> AmazonReport:
        raise NotImplementedError

    @abstractmethod
    def get_report_document(self, document_id: str) -> ReportDocument:
        raise NotImplementedError

    @abstractmethod
    def get_report_document_text(self, report_document_url: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_and_get_report_text(self, report_type: ReportType) -> str:
        raise NotImplementedError
