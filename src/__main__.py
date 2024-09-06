from sp_api.base import Marketplaces, ReportType

from src.main.reports import create_report, download_report
from sp_api.base.exceptions import SellingApiException
from src.main.exceptions import ReportCreationError
# GET_FBA_MYI_ALL_INVENTORY_DATA inventory
# GET_REFERRAL_FEE_PREVIEW_REPORT 403 forbined
# GET_FBA_STORAGE_FEE_CHARGES_DATA calceled
# GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA  есть нужный параметр но не полный список позиций


marketplaces = [
    # Marketplaces.IT,
    # Marketplaces.FR,
    # Marketplaces.ES,
    Marketplaces.DE,
    Marketplaces.GB,
]
report_type = ReportType.GET_FBA_MYI_ALL_INVENTORY_DATA

for marketplace in marketplaces:
    print('Start processing:', marketplace)
    try:
        report_id = create_report(marketplace=marketplace, report_type=report_type)
        download_report(report_id=report_id, marketplace=marketplace)
    except (SellingApiException, ReportCreationError,) as error:
        # [{'code': 'QuotaExceeded', 'message': 'You exceeded your quota for the requested resource.', 'details': ''}]
        print(error)