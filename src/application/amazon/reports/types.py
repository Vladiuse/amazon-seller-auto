from enum import Enum

from sp_api.base import ReportType as SpApiReportType


class ReportType(Enum):
    INVENTORY = SpApiReportType.GET_FBA_MYI_ALL_INVENTORY_DATA
    SALES = SpApiReportType.GET_SALES_AND_TRAFFIC_REPORT
    VENDOR_SALES = SpApiReportType.GET_VENDOR_REAL_TIME_SALES_REPORT
    FEE = SpApiReportType.GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA  # one report on all marketplaces
