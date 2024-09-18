from abc import abstractmethod, ABC
from sp_api.base import Marketplaces, ProcessingStatus, ReportType


class IAmazonReportCreator(ABC):

    @abstractmethod
    def create_report(self, report_type: ReportType) -> str:
        raise NotImplementedError
