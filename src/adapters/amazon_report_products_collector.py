from sp_api.base import Marketplaces, ReportType

from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct
from src.application.amazon.amazon_report_product_collector.interfaces.amazon_report_products_collector import (
    IAmazonReportProductsCollector,
)
from src.application.amazon.amazon_report_product_collector.interfaces.amazon_reports_collector import (
    IAmazonReportCollector,
)
from src.application.amazon.amazon_report_product_collector.interfaces.report_product_converner import (
    IReportProductConvertor,
)
from src.application.amazon.utils import get_get_by_marketplace_id


class AmazonReportProductsCollector(IAmazonReportProductsCollector):

    def __init__(
            self,
            report_collector: IAmazonReportCollector,
            report_convertor: IReportProductConvertor,
    ):
        self._report_collector = report_collector
        self._report_convertor = report_convertor

    def collect(self, report_type: ReportType, marketplace: Marketplaces) -> list[AmazonReportProduct]:
        report_text = self._report_collector.collect(report_type=report_type, save_report=True)
        marketplace_country = get_get_by_marketplace_id(marketplace)
        return self._report_convertor.convert(
            report_document_text=report_text,
            marketplace_country=marketplace_country,
        )
