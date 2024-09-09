from sp_api.base import Marketplaces, ReportType

from src.application.amazon_product_collector.dto.product import AmazonReportProduct
from src.application.amazon_product_collector.interfaces.amazon_products_collector import IAmazonReportProductsCollector
from src.application.amazon_product_collector.interfaces.amazon_reports_collector import IAmazonReportCollector
from src.application.amazon_product_collector.interfaces.report_product_converner import IReportProductConvertor
from src.application.amazon_product_collector.utils import get_get_by_marketplace_id


class AmazonReportProductsCollector(IAmazonReportProductsCollector):

    def __init__(
            self,
            report_collector: IAmazonReportCollector,
            report_convertor: IReportProductConvertor,
    ):
        self._report_collector = report_collector
        self._report_convertor = report_convertor

    def collect(self, report_type: ReportType, marketplace: Marketplaces) -> list[AmazonReportProduct]:
        collector = self._report_collector(marketplace=marketplace)
        report_text = collector.create_and_get_report_text(report_type=report_type)
        marketplace_country = get_get_by_marketplace_id(marketplace)
        return self._report_convertor().convert(
            report_document_text=report_text,
            marketplace_country=marketplace_country,
        )
