from abc import ABC, abstractmethod

from sp_api.base import ReportType as SpReportType, Marketplaces as SpMarketplaces

from src.application.amazon.amazon_reports.dto.report import AmazonReportDocument
from src.application.amazon.amazon_reports.dto.product import AmazonReportProduct


class IAmazonReportProvider(ABC):

    @abstractmethod
    def provide(self, report_type: SpReportType) -> AmazonReportDocument:
        raise NotImplementedError


class IAmazonReportDocumentProductProvider(ABC):

    @abstractmethod
    def collect(self, report_document: AmazonReportDocument, marketplace: SpMarketplaces) -> list[AmazonReportProduct]:
        raise NotImplementedError
