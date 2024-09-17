import csv
import io

from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct
from src.application.amazon.amazon_report_product_collector.interfaces.report_product_converner import (
    IReportProductConvertor,
)
from src.application.amazon.dto import MarketplaceCountry


class ReportProductConverter(IReportProductConvertor):

    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[AmazonReportProduct]:
        products = []
        reader = csv.DictReader(io.StringIO(report_document_text), delimiter='\t')
        for row in reader:
            product = AmazonReportProduct(
                asin=row['asin'],
                name=row['product-name'],
                marketplace_country=marketplace_country,
                sku=row['sku'],
                available=int(row['afn-fulfillable-quantity']),
                inbound=int(row['afn-inbound-shipped-quantity']),
                featured_offer=row['your-price'],
                inbound_receiving_qty=int(row['afn-inbound-receiving-quantity']),
            )
            products.append(product)
        return products
