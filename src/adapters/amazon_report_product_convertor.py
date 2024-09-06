import csv
import os

from src.application.amazon_product_collector.dto.product import AmazonReportProduct
from src.application.amazon_product_collector.interfaces.report_product_converner import IReportProductConvertor


class ReportProductConvertor(IReportProductConvertor):

    def convert(self, report_path: str) -> list[AmazonReportProduct]:
        file_name = os.path.basename(report_path)
        marketplace_country = file_name[:2]
        products = []
        with open(report_path) as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                product = AmazonReportProduct(marketplace_country=marketplace_country, **row)
                products.append(product)
        return products
