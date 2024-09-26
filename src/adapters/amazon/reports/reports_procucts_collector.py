import logging
from dataclasses import dataclass

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.reports.dto.product import AmazonReportProduct
from src.application.amazon.reports.interfaces.report_document_product_provider import (
    IAmazonReportDocumentProductProvider,
)
from src.application.amazon.reports.interfaces.reports_procucts_collector import IAmazonReportsProductsCollector


@dataclass
class AmazonReportsProductsCollector(IAmazonReportsProductsCollector):
    amazon_report_document_product_provider: IAmazonReportDocumentProductProvider

    def collects(self, marketplace_countries: list[MarketplaceCountry]) -> list[AmazonReportProduct]:
        products_from_all_marketplaces = []
        for marketplace_country in marketplace_countries:
            products_from_marketplace = self.amazon_report_document_product_provider.provide(
                marketplace_country=marketplace_country,
            )
            logging.info('%s, products found: %s', marketplace_country, len(products_from_marketplace))
            products_from_all_marketplaces.extend(products_from_marketplace)
        return products_from_all_marketplaces
