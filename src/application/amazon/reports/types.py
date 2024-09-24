from enum import Enum

from sp_api.base import ReportType as SpApiReportType


class ReportType(Enum):
    INVENTORY = SpApiReportType.GET_FBA_MYI_ALL_INVENTORY_DATA
    SALES = SpApiReportType.GET_SALES_AND_TRAFFIC_REPORT
    VENDOR_SALES = SpApiReportType.GET_VENDOR_REAL_TIME_SALES_REPORT
    # VENDOR_SALES = SpApiReportType.GET_VENDOR_SALES_REPORT

