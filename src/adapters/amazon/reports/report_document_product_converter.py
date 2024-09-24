import csv
import io
import json
from collections import defaultdict

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.reports.dto.product import (
    AmazonInventoryReportProduct,
    SaleReportProduct,
    VendorSaleProduct,
)
from src.application.amazon.reports.interfaces.report_product_converner import (
    IReportProductConvertor,
    ISalesReportDocumentConvertor,
    IVendorSalesConverter,
)


class InventoryReportDocumentConverter(IReportProductConvertor):

    def convert(self, report_document_text: str, marketplace_country: MarketplaceCountry) -> list[
        AmazonInventoryReportProduct]:
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


class VendorSalesReportConverter(IVendorSalesConverter):

    def convert(self, report_document_text, marketplace_country: MarketplaceCountry) -> list[VendorSaleProduct]:
        vendor_sales = []
        data = json.loads(report_document_text)
        asins = defaultdict(int)
        for sale_item in data['reportData']:
            asins[sale_item['asin']] +=sale_item['orderedUnits']
        for asin, ordered_units in asins.items():
            vendor_sale_item = VendorSaleProduct(
                asin=asin,
                ordered_units=ordered_units,
                marketplace_country=marketplace_country,
            )
            vendor_sales.append(vendor_sale_item)
        return vendor_sales
