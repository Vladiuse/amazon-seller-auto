from dataclasses import dataclass

from src.application.amazon.pages.dto.product import AmazonProduct
from src.application.amazon.pages.interfaces.page_provider import IAmazonProductPageProvider
from src.application.amazon.pages.interfaces.product_collector import IAmazonProductCollector
from src.application.amazon.pages.interfaces.product_converter import IAmazonProductConvertor
from src.application.amazon.common.types import Asin, MarketplaceCountry


@dataclass
class AmazonProductCollector(IAmazonProductCollector):
    product_convertor: IAmazonProductConvertor
    product_page_provider: IAmazonProductPageProvider

    def collect(self, asin: Asin, marketplace_country: MarketplaceCountry) -> AmazonProduct:
        html = self.product_page_provider.provide(asin=asin, marketplace_country=marketplace_country)
        return self.product_convertor.convert(html=html, asin=asin.value, marketplace_country=marketplace_country.value)
