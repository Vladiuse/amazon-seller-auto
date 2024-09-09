import csv
import io

from sp_api.base import Marketplaces

from src.application.amazon_product_collector.dto.product import AmazonReportProduct
from src.application.amazon_product_collector.interfaces.report_product_converner import IReportProductConvertor


class ReportProductConvertor(IReportProductConvertor):

    def convert(self, report_document_text: str, marketplace: Marketplaces) -> list[AmazonReportProduct]:
        marketplace_country = marketplace.marketplace_id
        products = []
        reader = csv.DictReader(io.StringIO(report_document_text), delimiter='\t')
        for row in reader:
            product = AmazonReportProduct(marketplace_country=marketplace_country, **row)
            products.append(product)
        return products
