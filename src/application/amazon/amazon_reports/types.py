from enum import Enum

from sp_api.base import ReportType as SPReportType


class ReportType(Enum):
    INVENTORY = SPReportType.GET_FBA_MYI_ALL_INVENTORY_DATA
    SALES = SPReportType.GET_SALES_AND_TRAFFIC_REPORT

