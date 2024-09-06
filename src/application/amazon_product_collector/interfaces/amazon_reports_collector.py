from dataclasses import dataclass
from abc import ABC, abstractmethod
from sp_api.base import ReportType, Marketplaces


class IAmazonReportCollector(ABC):

    @abstractmethod
    def get_report(self, report_type:ReportType, marketplace:Marketplaces) -> str:
        raise NotImplementedError