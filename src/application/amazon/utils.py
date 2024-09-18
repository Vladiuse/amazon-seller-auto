import logging
import os
from time import sleep

from sp_api.base import Marketplaces, ReportType

from src.application.amazon.common.types import Asin, MarketplaceCountry
from src.main.config import ACTIVE_ASINS_FILE_PATH, AMAZON_PRODUCT_PAGES_DIR, REPORTS_DIR
from src.main.exceptions import MaxTriesError


def retry(attempts: int = 3, delay: float = 10, exceptions: tuple[type[BaseException]] | None = None):
    if exceptions is None:
        exceptions = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if type(e) not in exceptions:
                        raise e
                    logging.info('Sleeping')
                    sleep(delay)
            raise MaxTriesError(f'func_name: {func.__name__}')

        return wrapper

    return decorator


def save_amazon_product_page(html: str, asin: Asin, marketplace_country: MarketplaceCountry) -> None:
    file_path = os.path.join(AMAZON_PRODUCT_PAGES_DIR,
                             f'{marketplace_country.value}_{asin.value}.html')
    with open(file_path, 'w') as file:
        file.write(html)


def save_amazon_report(report_text: str, report_type: ReportType, marketplace_id: str) -> None:
    report_file_name = f'{marketplace_id}_{report_type.value}.csv'
    report_file_path = os.path.join(REPORTS_DIR, report_file_name)
    with open(report_file_path, 'w') as file:
        file.write(report_text)


def get_marketplace_by_id(marketplace: Marketplaces) -> MarketplaceCountry:
    key = {
        'A13V1IB3VIYZZH': 'FR',
        'A1RKKUPIHCS9HS': 'ES',
        'A1PA6795UKMFR9': 'DE',
        'APJ6JRA9NG5V4': 'IT',
        'A1F83G8C2ARO7P': 'UK',
    }[marketplace.marketplace_id]
    return getattr(MarketplaceCountry, key)


def get_active_asins(return_string=False) -> list[Asin | str]:
    asins = []
    with open(ACTIVE_ASINS_FILE_PATH) as file:
        for line in file:
            asin_str = line.strip()
            if asin_str != '':
                asin = Asin(value=asin_str)
                asins.append(asin)
    if return_string:
        return [asin.value for asin in asins]
    return asins


def get_marketplace_url(marketplace_country: MarketplaceCountry) -> str:
    return {
        'FR': 'https://www.amazon.fr/',
        'IT': 'https://www.amazon.it/',
        'DE': 'https://www.amazon.de/',
        'GB': 'https://www.amazon.co.uk/',
        'UK': 'https://www.amazon.co.uk/',
        'ES': 'https://www.amazon.es/',
    }[marketplace_country.value]
