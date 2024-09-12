from time import sleep

from sp_api.base import Marketplaces

from src.application.amazon.amazon_report_product_collector.dto.product import MarketplaceCountry
from src.application.amazon.dto import Asin
from src.main.amazonconfig import ACTIVE_ASINS_FILE_PATH
from src.main.exceptions import MaxTriesError


def retry(attempts: int = 3, delay: float = 10, exceptions: list[type[BaseException]] = None):
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
                    print('Sleeping')
                    sleep(delay)
            raise MaxTriesError(func.__name__)

        return wrapper

    return decorator


# TODO
# норм так делать? тк в Marketplaces не могу код нео получить
def get_get_by_marketplace_id(marketplace: Marketplaces) -> MarketplaceCountry:
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
