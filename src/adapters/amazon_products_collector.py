import csv
import os

from src.application.amazon_product_collector.dto.product import AmazonProduct
from src.application.amazon_product_collector.interfaces.amazon_products_collector import IAmazonReportProductsCollector


class AmazonReportProductsCollector(IAmazonReportProductsCollector):

    def collect(self, report_path: str) -> list[AmazonProduct]:
        file_name = os.path.basename(report_path)
        marketplace_country = file_name[:2]
        products = []
        with open(report_path) as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                product = AmazonProduct(marketplace_country=marketplace_country, **row)
                products.append(product)
        return products
