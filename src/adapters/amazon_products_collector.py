from sp_api.base import Marketplaces, ReportType

from src.application.amazon_product_collector.dto.product import AmazonReportProduct
from src.application.amazon_product_collector.interfaces.amazon_products_collector import IAmazonReportProductsCollector
from src.application.amazon_product_collector.interfaces.amazon_reports_collector import IAmazonReportCollector
from src.application.amazon_product_collector.interfaces.report_product_converner import IReportProductConvertor


class AmazonReportProductsCollector(IAmazonReportProductsCollector):

    def __init__(
            self,
            report_collector: IAmazonReportCollector,
            report_convertor: IReportProductConvertor,
    ):
        self._report_collector = report_collector
        self._report_convertor = report_convertor

    def collect(self, report_type: ReportType, marketplace: Marketplaces) -> list[AmazonReportProduct]:
        report_path = self._report_collector.get_report(report_type=report_type, marketplace=marketplace)
        return self._report_convertor.convert(report_path=report_path)
