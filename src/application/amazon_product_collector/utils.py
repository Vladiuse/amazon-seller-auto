from time import sleep

from sp_api.base import Marketplaces

from src.application.amazon_product_collector.dto.product import MarketplaceCountry


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
            return None   # TODO тут может резить ошибку тип MaxTryError?

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
    return MarketplaceCountry(key)
