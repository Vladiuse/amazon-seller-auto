from dataclasses import dataclass
from sp_api.base import ReportType, Marketplaces
from src.application.amazon_product_collector.interfaces.amazon_reports_collector import IAmazonReportCollector
from src.application.amazon_product_collector.dto.report import ReportDocument

@dataclass(frozen=True)
class BaseCollectAmazonReportDocumentUseCase:
    amazon_products_collector: IAmazonReportCollector

    def __call__(self, report_type: ReportType, marketplaces: list[Marketplaces]) -> list[ReportDocument]:
        raise NotImplementedError


class CollectAmazonReportDocumentUseCase(BaseCollectAmazonReportDocumentUseCase):

    def __call__(self, report_type: ReportType, marketplaces: list[Marketplaces]) -> list[ReportDocument]:
        reports = []
        for marketplace in marketplaces:
            collector = self.amazon_products_collector(marketplace=marketplace)
            report_id = collector.get_report()
            report = self.amazon_products_collector
