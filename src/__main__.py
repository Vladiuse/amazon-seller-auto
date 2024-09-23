import logging

from src.application.amazon.common.types import MarketplaceCountry
from src.application.usecase import CollectProductsAndSendToAirtableUseCase

logging.basicConfig(level=logging.INFO)

marketplace_countries = [
    MarketplaceCountry.IT,
    MarketplaceCountry.ES,
    MarketplaceCountry.DE,
    MarketplaceCountry.FR,
    MarketplaceCountry.UK,
]

use_case = CollectProductsAndSendToAirtableUseCase()
use_case.collect_and_send(marketplace_countries=marketplace_countries)
