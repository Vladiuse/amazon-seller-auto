from abc import ABC, abstractmethod

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.reports.dto.report import AmazonReportDocument
from src.application.amazon.reports.types import ReportType


class IAmazonReportProvider(ABC):

    @abstractmethod
    def provide(self,
                marketplace_country: MarketplaceCountry,
                report_type: ReportType,
                try_get_exists_report: bool = False,
                **kwargs,
                ) -> AmazonReportDocument:
        raise NotImplementedError
