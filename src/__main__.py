import logging

from sp_api.base import Marketplaces

from src.application.amazon.utils import get_active_asins
from src.application.usecase import CollectProductsAndSendToAirtableUseCase

logging.basicConfig(level=logging.INFO)
marketplaces = [
    Marketplaces.IT,
    Marketplaces.ES,
    Marketplaces.DE,
    Marketplaces.FR,
    Marketplaces.UK,
]
active_asins = get_active_asins(return_string=True)

use_case = CollectProductsAndSendToAirtableUseCase()
use_case.collect_and_send(marketplaces=marketplaces, active_asins=active_asins)
