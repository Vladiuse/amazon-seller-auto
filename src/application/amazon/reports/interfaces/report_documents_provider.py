from abc import ABC, abstractmethod

from src.application.amazon.reports.dto.report import AmazonReportDocument
from src.application.amazon.reports.types import ReportType


class IAmazonReportProvider(ABC):

    @abstractmethod
    def provide(self, report_type: ReportType, **kwargs) -> AmazonReportDocument:
        raise NotImplementedError
