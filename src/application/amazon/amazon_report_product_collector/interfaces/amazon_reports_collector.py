from abc import ABC, abstractmethod

from sp_api.base import ReportType

from src.application.amazon.amazon_report_product_collector.dto.report import AmazonReportDocument


class IAmazonReportCollector(ABC):

    @abstractmethod
    def collect(self, report_type: ReportType) -> AmazonReportDocument:
        raise NotImplementedError


class IAmazonReportDocumentProductCollector(ABC):

    @abstractmethod
    def collect(self, report_document: AmazonReportDocument) -> str:
        raise NotImplementedError
