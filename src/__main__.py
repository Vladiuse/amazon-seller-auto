import logging

from sp_api.base import Marketplaces, ReportType

from src.adapters.amazon_product_collector import AmazonProductCollectorFromSavedFile, AmazonProductCollector
from src.adapters.amazon_product_convertor import AmazonProductConvertor
from src.adapters.amazon_report_product_convertor import ReportProductConvertor
from src.adapters.amazon_report_products_collector import AmazonReportProductsCollector
from src.adapters.amazon_reports_collector import AmazonSavedReportCollector, AmazonReportCollector
from src.application.airtable_product_sender.interfaces.airtable_product_sender import AirTableProductSender
from src.application.amazon.amazon_product_collector.usecase import CollectAmazonProductsUseCase
from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct
from src.application.amazon.dto import Asin, MarketplaceCountry
from src.application.amazon.utils import get_active_asins

logging.basicConfig(level=logging.INFO)
marketplaces = [
    Marketplaces.IT,
    Marketplaces.ES,
    Marketplaces.DE,
    Marketplaces.FR,
    Marketplaces.UK,
]

products_from_reports: list[AmazonReportProduct] = []

# Report collect
for marketplace in marketplaces:
    logging.info(marketplace)
    report_type = ReportType.GET_FBA_MYI_ALL_INVENTORY_DATA
    collector = AmazonReportProductsCollector(
        # report_collector=AmazonSavedReportCollector(marketplace),  # TEST
        report_collector=AmazonReportCollector(marketplace),
        report_convertor=ReportProductConvertor(),
    )
    products = collector.collect(report_type=report_type, marketplace=marketplace)
    logging.info('collected %s', len(products))
    products_from_reports.extend(products)

logging.info('Total products collected: %s', len(products_from_reports))
active_asins = get_active_asins(return_string=True)

active_products: list[AmazonReportProduct] = []  # with transfer to airtable
for product in products_from_reports:
    if product.asin in active_asins:
        active_products.append(product)

logging.info('Total active_products: %s', len(active_products))

# load rating and reviews
unique_asins_to_parse: list[tuple[Asin, MarketplaceCountry]] = []
for product in active_products:
    asin = Asin(value=product.asin)
    item = (asin, product.marketplace_country)
    if item not in unique_asins_to_parse:
        unique_asins_to_parse.append(item)

logging.info('Total unique_asins_to_parse: %s', len(unique_asins_to_parse))

product_collector = CollectAmazonProductsUseCase(
    # product_collector=AmazonProductCollectorFromSavedFile(product_convertor=AmazonProductConvertor()),  # TEST
    product_collector=AmazonProductCollector(product_convertor=AmazonProductConvertor()),
)
products_from_pars = product_collector.collect(unique_asins_to_parse)
logging.info('Total parsed asins: %s', len(products_from_pars))

for product in active_products:
    for product_from_pars in products_from_pars:
        if product.asin == product_from_pars.asin.value and \
                product.marketplace_country == product_from_pars.marketplace_country:
            product.rating = product_from_pars.rating
            product.rating_reviews = product_from_pars.rating_reviews
            break

airtable_sender = AirTableProductSender()
airtable_sender.clean_table()
airtable_sender.send_products_to_table(
    products=active_products,
)
logging.info('\nEnd')
