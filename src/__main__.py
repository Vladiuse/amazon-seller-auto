import logging
from csv import DictWriter

from sp_api.base import Marketplaces, ReportType

from src.adapters.amazon_products_collector import AmazonReportProductsCollector
from src.adapters.amazon_report_product_convertor import ReportProductConvertor
from src.adapters.amazon_reports_collector import AmazonReportCollector
from src.application.amazon_product_collector.dto.product import AmazonReportProduct

logging.basicConfig(level=logging.INFO)


def write_products_in_file(products: list[AmazonReportProduct]) -> None:
    with open('products.csv', 'a') as file:
        fieldnames = list(AmazonReportProduct.model_fields.keys())
        print(fieldnames)
        writer = DictWriter(file, delimiter=',', quotechar='"', fieldnames=fieldnames)
        writer.writeheader()
        for i in products:
            writer.writerow(i.model_dump())


marketplaces = [
    # Marketplaces.IT,
    # Marketplaces.FR,
    # Marketplaces.ES,
    # Marketplaces.DE,
    Marketplaces.GB,
]
report_type = ReportType.GET_FBA_MYI_ALL_INVENTORY_DATA

collector = AmazonReportProductsCollector(
    report_collector=AmazonReportCollector,
    report_convertor=ReportProductConvertor,
)
for marketplace in marketplaces:
    products = []
    logging.info(marketplace)
    report_products = collector.collect(report_type=report_type, marketplace=marketplace)
    products.extend(report_products)

    logging.info(len(products))
    write_products_in_file(products)
