from enum import Enum


class MarketplaceCountry(Enum):
    FR = ('FR', 'https://www.amazon.fr/')
    IT = ('IT', 'https://www.amazon.it/')
    DE = ('DE', 'https://www.amazon.de/')
    GB = ('GB', 'https://www.amazon.co.uk/')
    UK = ('UK', 'https://www.amazon.co.uk/')
    ES = ('ES', 'https://www.amazon.es/')

    def __init__(self, country_code: str, url: str):
        self.country_code = country_code
        self.url = url

    def __str__(self):
        return self.country_code