from abc import ABC, abstractmethod

from src.application.airtable_product_sender.dto.product_table import MainTableProduct
from src.application.amazon.reports.dto.product import VendorSaleProduct


class IAirTableProductSender(ABC):


    @abstractmethod
    def send_products_to_table(self, products: list[MainTableProduct]) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_vendor_sales_data(self, items: list[VendorSaleProduct]) -> None:
        raise NotImplementedError