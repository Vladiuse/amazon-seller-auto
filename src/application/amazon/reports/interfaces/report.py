from abc import ABC, abstractmethod

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.reports.dto.report import AmazonReport, AmazonReportDocument
from src.application.amazon.reports.types import ReportType


class IAmazonReportCreator(ABC):

    @abstractmethod
    def create_report(self, credentials: dict, marketplace_country: MarketplaceCountry, report_type: ReportType,
                      **kwargs) -> str:
        raise NotImplementedError


class IAmazonReportGetter(ABC):

    @abstractmethod
    def get_report(self, credentials: dict, marketplace_country: MarketplaceCountry, report_id: str) -> AmazonReport:
        raise NotImplementedError

    @abstractmethod
    def get_today_reports(self,
                          credentials: dict,
                          marketplace_country: MarketplaceCountry,
                          report_type: ReportType,
                          ) -> list[AmazonReport]:
        raise NotImplementedError


class IAmazonReportDocumentGetter(ABC):

    @abstractmethod
    def get_report_document(self, credentials: dict, marketplace_country: MarketplaceCountry,
                            document_id: str) -> AmazonReportDocument:
        raise NotImplementedError
