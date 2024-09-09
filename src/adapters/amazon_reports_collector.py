import requests as req
from requests.exceptions import RequestException
from sp_api.api import Reports
from sp_api.base import Marketplaces, ReportType

from src.application.amazon_product_collector.dto.report import AmazonReport, ReportDocument
from src.application.amazon_product_collector.interfaces.amazon_reports_collector import IAmazonReportCollector
from src.application.amazon_product_collector.utils import retry
from src.main.config import credentials
from src.main.exceptions import ReportCreationError, ReportDocumentNotComplete, ReportStatusError


class AmazonReportCollector(IAmazonReportCollector):

    def __init__(self, marketplace: Marketplaces):
        self.marketplace = marketplace
        self.reports = Reports(credentials=credentials, marketplace=marketplace)

    @retry(
        attempts=5,
        delay=3 * 60,
        exceptions=[ReportCreationError],
    )
    def create_report(self, report_type: ReportType) -> str:
        print('create_report')
        data = self.reports.create_report(reportType=report_type)
        try:
            print(data.payload)
            return data.payload['reportId']
        except KeyError:
            raise ReportCreationError

    @retry(
        attempts=20,
        delay=30,
        exceptions=[ReportDocumentNotComplete, ],
    )
    def get_report(self, report_id: str) -> AmazonReport:
        print('get_report')
        data = self.reports.get_report(reportId=report_id)
        print(data.payload)
        report = AmazonReport(**data.payload)
        if report.is_complete():
            if report.is_document_created():
                return AmazonReport(**data.payload)
            raise ReportStatusError
        print('report not complete')
        raise ReportDocumentNotComplete

    def get_report_document(self, document_id: str) -> ReportDocument:
        print('get_report_document')
        data = self.reports.get_report_document(reportDocumentId=document_id)
        return ReportDocument(**data.payload)

    @retry(
        attempts=5,
        delay=10,
        exceptions=[RequestException],
    )
    def get_report_document_text(self, report_document_url: str) -> str:
        print('get_report_document_text')
        res = req.get(report_document_url)
        res.raise_for_status()
        return res.text

    @retry(
        attempts=3,
        delay=1,
        exceptions=[ReportStatusError, ],
    )
    def create_and_get_report_text(self, report_type: ReportType) -> str:
        print('create_and_get_report_text')
        report_id = self.create_report(report_type=report_type)
        report = self.get_report(report_id=report_id)
        report_document = self.get_report_document(document_id=report.document_id)
        return self.get_report_document_text(report_document.url)
