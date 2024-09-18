from abc import ABC, abstractmethod

from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct


class IAirTableProductSender(ABC):


    @abstractmethod
    def send_products_to_table(self, products: list[AmazonReportProduct]) -> None:
        raise NotImplementedError
