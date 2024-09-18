from sp_api.api import Reports as SpApiReports
from sp_api.base import ReportType

from src.application.amazon.amazon_report_product_collector.interfaces.amazon_report_creator import (
    IAmazonReportCreator,
    IAmazonReportDocumentGetter,
    IAmazonReportGetter,
)
from src.application.amazon.amazon_report_product_collector.interfaces.amazon_reports_collector import (
    IAmazonReportCollector,
)
from src.application.amazon.amazon_report_product_collector.usecase import GetExitingOrCreateAmazonReportUseCase
from src.application.amazon.utils import save_amazon_report


class AmazonReportDocumentTextCollector(IAmazonReportCollector):

    def __init__(self,
                 sp_api_reports: SpApiReports,
                 report_creator: IAmazonReportCreator,
                 report_getter: IAmazonReportGetter,
                 report_document_getter: IAmazonReportDocumentGetter,
                 ):
        self._sp_api_reports = sp_api_reports
        self._report_creator = report_creator
        self._report_getter = report_getter
        self._report_document_getter = report_document_getter

    def collect(self, report_type: ReportType, save_report: bool = False) -> str:
        report = GetExitingOrCreateAmazonReportUseCase(
            sp_api_reports=self._sp_api_reports,
            report_creator=self._report_creator,
            report_getter=self._report_getter,
        ).get_or_create_report(report_type=report_type)
        report_document = self._report_document_getter.get_report_document(document_id=report.document_id)
        report_document_text = self._report_document_getter.get_report_document_text(document_url=report_document.url)
        if save_report:
            save_amazon_report(report_text=report_document_text,
                               report_type=report_type,
                               marketplace_id=self._sp_api_reports.marketplace_id)
        return report_document_text

# class AmazonSavedReportCollector(AmazonReportTextCollector):
# 
#     def create_and_get_report_text(self, report_type: ReportType) -> str:
#         geo = str(self.marketplace).split('.')[-1]
#         file_name = f'{geo}_{report_type.value}.txt'
#         file_path = os.path.join(REPORTS_DIR, file_name)
#         with open(file_path) as file:
#             return file.read()
