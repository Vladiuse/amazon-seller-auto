import csv
import io

from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct
from src.application.amazon.amazon_report_product_collector.interfaces.report_product_converner import (
    IReportProductConvertor,
)
from src.application.amazon.dto import MarketplaceCountry


class ReportProductConvertor(IReportProductConvertor):

    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[AmazonReportProduct]:
        products = []
        reader = csv.DictReader(io.StringIO(report_document_text), delimiter='\t')
        for row in reader:
            product = AmazonReportProduct(marketplace_country=marketplace_country, **row)
            products.append(product)
        return products
