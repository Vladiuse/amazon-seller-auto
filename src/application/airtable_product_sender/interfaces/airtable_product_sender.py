from abc import ABC, abstractmethod

from src.application.airtable_product_sender.dto.table_records import AmazonProductRecord
from src.application.amazon.reports.dto.product import VendorSaleProduct


class IAirTableProductSender(ABC):

    @abstractmethod
    def send_products_to_table(self, products: list[AmazonProductRecord]) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_vendor_sales_data(self, items: list[VendorSaleProduct]) -> None:
        raise NotImplementedError
