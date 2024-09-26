from bs4 import BeautifulSoup

from src.application.amazon.common.types import MarketplaceCountry
from src.application.amazon.pages.dto.product import AmazonPageProduct
from src.application.amazon.pages.interfaces.product_converter import IAmazonProductConverter
from src.main.exceptions import HtmlElementNotFound, ParserError


class AmazonProductConverter(IAmazonProductConverter):

    def convert(self, html: str, asin: str, marketplace_country: MarketplaceCountry) -> AmazonPageProduct:
        soup = BeautifulSoup(html, 'lxml')
        rating_reviews = self.__get_rating_reviews(soup)
        rating = self.__get_rating(soup)
        return AmazonPageProduct(
            rating_reviews=rating_reviews,
            rating=rating,
            asin=asin,
            marketplace_country=marketplace_country,
        )

    def __get_rating_reviews(self, soup: BeautifulSoup) -> int:
        reviews_block = soup.find('span', attrs={'id': 'acrCustomerReviewText', })
        if reviews_block is None:
            raise HtmlElementNotFound
        try:
            return self.__get_numbers(string=reviews_block.text)
        except ValueError:
            raise ParserError('Cant get reviews')

    def __get_rating(self, soup: BeautifulSoup) -> float:
        rate_block = soup.find('span', attrs={'class': 'reviewCountTextLinkedHistogram', })
        if rate_block is None:
            raise HtmlElementNotFound
        rating = rate_block.find('span', attrs={'class': 'a-size-base a-color-base', })
        if rating is None:
            raise HtmlElementNotFound
        rating_text = rating.text.strip().replace(',', '.')
        try:
            return float(rating_text)
        except ValueError:
            raise ParserError('Cant get rating')

    def __get_numbers(self, string: str) -> int:
        nums = ''
        for char in string:
            if char.isdigit():
                nums = nums + char
        return int(nums)
