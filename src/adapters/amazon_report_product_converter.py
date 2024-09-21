import csv
import gzip
import io
import json

from sp_api.base import ReportType

from src.application.amazon.amazon_reports.dto.product import AmazonInventoryReportProduct, SaleReportProduct
from src.application.amazon.amazon_reports.interfaces.report_product_converner import (
    IReportProductConvertor,
    ISalesReportDocumentConvertor,
)
from src.application.amazon.common.types import MarketplaceCountry



class FBAReportDocumentConverter(IReportProductConvertor):

    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[AmazonInventoryReportProduct]:
        products = []
        reader = csv.DictReader(io.StringIO(report_document_text), delimiter='\t')
        for row in reader:
            product = AmazonInventoryReportProduct(
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


class SalesReportDocumentConvertor(ISalesReportDocumentConvertor):

    def convert(self, report_document_text, marketplace_country: MarketplaceCountry) -> list[SaleReportProduct]:
        data = json.loads(report_document_text)
        products = []
        for item in data['salesAndTrafficByAsin']:
            sale_report_product = SaleReportProduct(
                asin=item['childAsin'],
                sku=item['sku'],
                units_ordered=item['salesByAsin']['unitsOrdered'],
                marketplace_country=marketplace_country,
            )
            products.append(sale_report_product)
        return products


def get_report_converters(report_type: ReportType) -> object:
    return {
        ReportType.GET_FBA_MYI_ALL_INVENTORY_DATA: {
            'content_converter': 'xxx',
            'converter': 'xxx',
        },
        ReportType.GET_SALES_AND_TRAFFIC_REPORT: {
            'content_converter': 'xxx',
            'converter': 'xxx',
        },
    }[report_type]
