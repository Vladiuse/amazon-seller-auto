from dataclasses import dataclass

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.pages.dto.product import AmazonPageProduct
from src.application.amazon.pages.interfaces.page_product_provider import IAmazonProductProvider
from src.application.amazon.pages.interfaces.page_provider import IAmazonProductPageProvider
from src.application.amazon.pages.interfaces.product_converter import IAmazonProductConvertor
from src.application.amazon.utils import save_amazon_product_page


@dataclass
class AmazonProductProvider(IAmazonProductProvider):
    product_convertor: IAmazonProductConvertor
    product_page_provider: IAmazonProductPageProvider

    def collect(self, asin: str, marketplace_country: MarketplaceCountry) -> AmazonPageProduct:
        html = self.product_page_provider.provide(asin=asin, marketplace_country=marketplace_country)
        save_amazon_product_page(html=html, asin=asin, marketplace_country=marketplace_country)
        return self.product_convertor.convert(html=html, asin=asin, marketplace_country=marketplace_country)
