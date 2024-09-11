from bs4 import BeautifulSoup

from src.application.amazon_product_collector.dto.product import AmazonProduct
from src.application.amazon_product_collector.interfaces.product_converter import IAmazonProductConvertor
from src.main.exceptions import HtmlElementNotFound


def get_numbers(string: str) -> int:
    nums = ''
    for char in string:
        if char.isdigit():
            nums = nums + char
    return int(nums)


class AmazonProductConvertor(IAmazonProductConvertor):

    def convert(self, html: str) -> AmazonProduct:
        soup = BeautifulSoup(html, 'lxml')
        reviews_total = self._get_reviews_total(soup)
        rating = self._get_rating(soup)
        return AmazonProduct(reviews_total=reviews_total, rating=rating)

    def _get_reviews_total(self, soup: BeautifulSoup) -> int:
        reviews_block = soup.find('span', attrs={'id': 'acrCustomerReviewText'})
        if reviews_block is None:
            raise HtmlElementNotFound
        return get_numbers(reviews_block.text)

    def _get_rating(self, soup: BeautifulSoup) -> float:
        rate_block = soup.find('span', attrs={'class': 'reviewCountTextLinkedHistogram'})
        if rate_block is None:
            raise HtmlElementNotFound
        rating = rate_block.find('span', attrs={'class': 'a-size-base a-color-base'})
        if rating is None:
            raise HtmlElementNotFound
        rating_text = rating.text.strip().replace(',', '.')
        return float(rating_text)
