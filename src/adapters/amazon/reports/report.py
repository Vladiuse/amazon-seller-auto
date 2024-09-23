import logging
from datetime import datetime

import requests
from requests.exceptions import RequestException
from sp_api.api import Reports as SpApiReports
from sp_api.base import Marketplaces as SpMarketplaces
from sp_api.base import ProcessingStatus
from sp_api.base.exceptions import SellingApiRequestThrottledException

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.reports.dto.report import AmazonReport, AmazonReportDocument
from src.application.amazon.reports.interfaces.report import (
    IAmazonReportCreator,
    IAmazonReportDocumentGetter,
    IAmazonReportGetter,
)
from src.application.amazon.reports.types import ReportType
from src.application.amazon.utils import retry
from src.main.config import config
from src.main.exceptions import ReportDocumentNotComplete, ReportStatusError

amazon_credentials = {
    'refresh_token': config.amazon_config.SP_API_REFRESH_TOKEN,
    'lwa_app_id': config.amazon_config.LWA_CLIENT_ID,
    'lwa_client_secret': config.amazon_config.LWA_CLIENT_SECRET,
}


class AmazonReportCreator(IAmazonReportCreator):

    @retry(
        attempts=5,
        delay=3 * 60,
        exceptions=(SellingApiRequestThrottledException,),
    )
    def create_report(self, marketplace_country: MarketplaceCountry, report_type: ReportType, **kwargs) -> str:
        marketplace = getattr(SpMarketplaces, marketplace_country.value)
        sp_api_reports = SpApiReports(credentials=amazon_credentials, marketplace=marketplace)
        data = sp_api_reports.create_report(reportType=report_type.value, **kwargs)
        logging.info(data.payload)
        return data.payload['reportId']


class AmazonReportGetter(IAmazonReportGetter):

    @retry(
        attempts=20,
        delay=30,
        exceptions=(ReportDocumentNotComplete,),
    )
    def get_report(self,marketplace_country: MarketplaceCountry, report_id: str) -> AmazonReport:
        marketplace = getattr(SpMarketplaces, marketplace_country.value)
        sp_api_reports = SpApiReports(credentials=amazon_credentials, marketplace=marketplace)
        data = sp_api_reports.get_report(reportId=report_id)
        logging.info(data.payload)
        report = AmazonReport(**data.payload)
        if not report.is_complete():
            raise ReportDocumentNotComplete
        if report.is_document_created():
            return AmazonReport(**data.payload)
        logging.error('Report not created \n %s', data.payload)
        raise ReportStatusError

    @retry(
        attempts=3,
        delay=10,
        exceptions=(SellingApiRequestThrottledException,),
    )
    def get_today_reports(self, marketplace_country: MarketplaceCountry, report_type: ReportType) -> list[AmazonReport]:
        marketplace = getattr(SpMarketplaces, marketplace_country.value)
        sp_api_reports = SpApiReports(credentials=amazon_credentials, marketplace=marketplace)
        date = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0).isoformat()
        data = sp_api_reports.get_reports(
            reportTypes=[report_type.value, ],
            processingStatuses=[ProcessingStatus.DONE, ],
            createdSince=date,
        )
        logging.info(data.payload)
        return [AmazonReport(**report_data) for report_data in data.payload['reports']]


class AmazonReportDocumentGetter(IAmazonReportDocumentGetter):

    @retry(
        attempts=3,
        delay=20,
        exceptions=(SellingApiRequestThrottledException,),
    )
    def get_report_document(self, marketplace_country:MarketplaceCountry ,document_id: str) -> AmazonReportDocument:
        marketplace = getattr(SpMarketplaces, marketplace_country.value)
        sp_api_reports = SpApiReports(credentials=amazon_credentials, marketplace=marketplace)
        data = sp_api_reports.get_report_document(reportDocumentId=document_id)
        return AmazonReportDocument(**data.payload)

