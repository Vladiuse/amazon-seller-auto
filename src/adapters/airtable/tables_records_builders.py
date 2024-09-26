from src.application.airtable_product_sender.dto.table_records import AmazonProductRecord, VendorSalesRecord
from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.pages.dto.product import AmazonPageProduct
from src.application.amazon.reports.dto.product import (
    AmazonInventoryReportProduct,
    FeeAmazonProduct,
    SaleReportProduct,
    VendorSaleProduct,
)


class MainTableRecordsBuilder:

    def __init__(self):
        self.items = {}

    def __get_record(self, asin: str, sku: str, marketplace_country: MarketplaceCountry) -> AmazonProductRecord:
        key = self.__get_key(asin=asin, sku=sku, marketplace_country=marketplace_country)
        try:
            record = self.items[key]
        except KeyError:
            record = AmazonProductRecord(asin=asin, sku=sku, marketplace_country=marketplace_country)
            self.items.update({
                key: record,
            })
        return record

    def __get_key(self, asin: str, sku: str, marketplace_country: MarketplaceCountry) -> str:
        return f'{asin}_{sku}_{marketplace_country.value}'

    def add_inventory_data(self, items: list[AmazonInventoryReportProduct]) -> None:
        for inventory_item in items:
            record = self.__get_record(
                asin=inventory_item.asin,
                sku=inventory_item.sku,
                marketplace_country=inventory_item.marketplace_country,
            )
            record.name = inventory_item.name
            record.available = inventory_item.available
            record.inbound = inventory_item.inbound
            record.featured_offer = inventory_item.featured_offer
            record.inbound_receiving_qty = inventory_item.inbound_receiving_qty
            record.available = inventory_item.available

    def add_sales_data(self, items: list[SaleReportProduct]) -> None:
        for sale_item in items:
            record = self.__get_record(
                asin=sale_item.asin,
                sku=sale_item.sku,
                marketplace_country=sale_item.marketplace_country,
            )
            record.units_ordered = sale_item.units_ordered

    def add_rating_data(self, items: list[AmazonPageProduct]) -> None:
        for rating_item in items:
            for record in self.items.values():
                if record.asin == rating_item.asin and record.marketplace_country == rating_item.marketplace_country:
                    record.rating = rating_item.rating
                    record.rating_reviews = rating_item.rating_reviews

    def add_fee_data(self, items: list[FeeAmazonProduct]) -> None:
        for fee_product in items:
            record = self.__get_record(
                asin=fee_product.asin,
                sku=fee_product.sku,
                marketplace_country=fee_product.marketplace_country,
            )
            record.fba_fee = fee_product.fba_fee

    def get_unique_asins_geo_pairs(self) -> list[tuple[str, MarketplaceCountry]]:
        result = []
        for item in self.items.values():
            pair = (item.asin, item.marketplace_country)
            if pair not in result:
                result.append(pair)
        return result


class VendorSalesRecordsBuilder:

    def __init__(self):
        self.items = []

    def add_vendor_sales_data(self, items: list[VendorSaleProduct]) -> None:
        for item in items:
            record = VendorSalesRecord(
                asin=item.asin,
                ordered_units=item.ordered_units,
                marketplace_country=item.marketplace_country,
            )
            self.items.append(record)
