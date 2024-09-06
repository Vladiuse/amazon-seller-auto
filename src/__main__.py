from sp_api.base import Marketplaces, ReportType

from src.main.reports import create_report, download_report
from sp_api.base.exceptions import SellingApiException
from src.main.exceptions import ReportCreationError
# GET_FBA_MYI_ALL_INVENTORY_DATA inventory
# GET_REFERRAL_FEE_PREVIEW_REPORT 403 forbined
# GET_FBA_STORAGE_FEE_CHARGES_DATA calceled
# GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA  есть нужный параметр но не полный список позиций
ACTIVE_IDS = [
    'B09GFLXSRF'
    'B09W1GZMR1',
    'B0BQMSMZJ3',
    'B09GFQQ1CM',
    'B0BK1DZGND',
    'B0BK1KDS19',
    'B09R1YR2V2',
    'B09YCZ3VYV',
    'B09HVCKFTB',
    'B091CYLSNF',
    'B0BK196QNQ',
    'B0BK1572HN',
    'B0B5GN86QG',
    'B0BJZZCVQ1',
    'B0BJZYJTVX',
    'B0CLRR1WWK',
    'B0BK9NP2XP',
    'B0BK9Q8G2T',
    'B0CBQ9FMLL',
    'B0CBQCHTJ9',
]

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