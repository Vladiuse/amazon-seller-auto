from abc import ABC, abstractmethod

from src.application.amazon.amazon_reports.dto.product import AmazonInventoryReportProduct


class IAirTableProductSender(ABC):


    @abstractmethod
    def send_products_to_table(self, products: list[AmazonInventoryReportProduct]) -> None:
        raise NotImplementedError
