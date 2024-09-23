from abc import ABC, abstractmethod

from src.application.airtable_product_sender.dto.product_table import MainTableProduct


class IAirTableProductSender(ABC):


    @abstractmethod
    def send_products_to_table(self, products: list[MainTableProduct]) -> None:
        raise NotImplementedError
