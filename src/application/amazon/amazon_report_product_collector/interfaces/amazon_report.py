from abc import ABC, abstractmethod

from sp_api.base import ReportType

from src.application.amazon.amazon_report_product_collector.dto.report import AmazonReport, AmazonReportDocument


class IAmazonReportCreator(ABC):

    @abstractmethod
    def create_report(self, report_type: ReportType) -> str:
        raise NotImplementedError


class IAmazonReportGetter(ABC):

    @abstractmethod
    def get_report(self, report_id: str) -> AmazonReport:
        raise NotImplementedError

    @abstractmethod
    def get_today_reports(self, report_type: ReportType) -> list[AmazonReport]:
        raise NotImplementedError

class IAmazonReportDocumentGetter(ABC):

    @abstractmethod
    def get_report_document(self, document_id: str) -> AmazonReportDocument:
        raise NotImplementedError

    @abstractmethod
    def get_report_document_text(self, document_url: str) -> str:
        raise NotImplementedError