from pprint import pprint
from time import sleep

from sp_api.api import Reports
from sp_api.base import Marketplaces, ProcessingStatus, ReportType

from src.main.config import credentials
from src.main.exceptions import ReportCreationError


def create_report(marketplace: Marketplaces, report_type: ReportType) -> str:
    res = Reports(credentials=credentials, marketplace=marketplace)
    data = res.create_report(reportType=report_type)
    pprint(data.payload)
    return data.payload.get('reportId')


def download_report(report_id: str, marketplace: Marketplaces) -> str:
    reports = Reports(credentials=credentials, marketplace=marketplace)
    data = reports.get_report(reportId=report_id)
    pprint(data.payload)
    # {'createdTime': '2024-09-06T10:46:51+00:00',
    #  'dataEndTime': '2024-09-06T10:46:51+00:00',
    #  'dataStartTime': '2024-09-06T10:46:51+00:00',
    #  'marketplaceIds': ['A1RKKUPIHCS9HS'],
    #  'processingStatus': 'IN_QUEUE',
    #  'reportId': '1142691019972',
    #  'reportType': 'GET_FBA_MYI_ALL_INVENTORY_DATA'}

    report_type = data.payload.get('reportType')
    while data.payload.get('processingStatus') not in [ProcessingStatus.DONE, ProcessingStatus.FATAL,
                                                       ProcessingStatus.CANCELLED]:
        sleep(10)
        print('Sleeping...')
        data = reports.get_report(reportId=report_id)

    if data.payload.get('processingStatus') in [ProcessingStatus.FATAL, ProcessingStatus.CANCELLED]:
        error_data = str(data.payload)
        raise ReportCreationError(error_data)
    report_data = reports.get_report_document(data.payload['reportDocumentId'])
    pprint(report_data.payload)
    report_path = f'{marketplace.name}_{report_type}.csv'
    with open(report_path, 'w', encoding='iso-8859-1') as file:
        reports.get_report_document(
            report_data.payload.get('reportDocumentId'),
            download=True,
            file=file,
            character_code='iso-8859-1',
        )
    return report_path
