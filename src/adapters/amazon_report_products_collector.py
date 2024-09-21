from dataclasses import dataclass

from sp_api.base import Marketplaces, ReportType

from src.application.amazon.amazon_reports.dto.product import AmazonInventoryReportProduct
from src.application.amazon.amazon_reports.interfaces.amazon_report_products_collector import (
    IAmazonReportProductsCollector,
)
from src.application.amazon.amazon_reports.interfaces.amazon_reports_collector import (
    IAmazonReportProvider,
)
from src.application.amazon.amazon_reports.interfaces.report_product_converner import (
    IReportProductConvertor,
)
from src.application.amazon.utils import get_marketplace_country


@dataclass
class AmazonReportProductsCollector(IAmazonReportProductsCollector):
    report_collector: IAmazonReportProvider
    report_convertor: IReportProductConvertor

    def collect(self, report_type: ReportType, marketplace: Marketplaces) -> list[AmazonInventoryReportProduct]:
        report_text = self.report_collector.provide(report_type=report_type, save_report=True)
        marketplace_country = get_marketplace_country(marketplace)
        return self.report_convertor.convert(
            report_document_text=report_text,
            marketplace_country=marketplace_country,
        )
