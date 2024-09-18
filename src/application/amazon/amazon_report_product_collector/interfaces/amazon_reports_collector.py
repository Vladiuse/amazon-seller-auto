from abc import ABC, abstractmethod

from sp_api.base import ReportType


class IAmazonReportCollector(ABC):

    @abstractmethod
    def collect(self, report_type: ReportType, save_report: bool = False) -> str:
        raise NotImplementedError
