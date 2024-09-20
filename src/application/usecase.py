import logging

from sp_api.base import Marketplaces

from src.adapters.airtable.airtable_product_sender import AirTableProductSender
from src.adapters.amazon_page_provider import AmazonProductPageFileReader
from src.adapters.amazon_product_collector import AmazonProductCollector
from src.adapters.amazon_product_converter import AmazonProductConverter
from src.adapters.amazon_request_sender import AmazonZenRowsRequestSender
from src.application.airtable_product_sender.usecase import UpdateAmazonProductsTableUseCase
from src.application.amazon.amazon_product_collector.usecase import CollectAmazonProductsUseCase
from src.application.amazon.amazon_report_product_collector.dto.product import AmazonReportProduct
from src.application.amazon.amazon_report_product_collector.usecase import CollectFBAInventoryReportProductsUseCase
from src.application.amazon.common.types import Asin, MarketplaceCountry
from src.main.config import AMAZON_PRODUCT_PAGES_DIR


class CollectProductsAndSendToAirtableUseCase:

    def collect_and_send(self, marketplaces: list[Marketplaces], active_asins: list[str]) -> None:

        # Report collect
        report_collector = CollectFBAInventoryReportProductsUseCase()
        products_from_reports: list[AmazonReportProduct] = report_collector.collect(marketplaces=marketplaces)
        logging.info('Total products collected: %s', len(products_from_reports))
        active_products: list[AmazonReportProduct] = []  # with transfer to airtable
        for product in products_from_reports:
            if product.asin in active_asins:
                active_products.append(product)
        logging.info('Total active_products: %s', len(active_products))

        # get active asins to parse
        unique_asins_to_parse: list[tuple[Asin, MarketplaceCountry]] = []
        for product in active_products:
            asin = Asin(value=product.asin)
            item = (asin, product.marketplace_country)
            if item not in unique_asins_to_parse:
                unique_asins_to_parse.append(item)
        logging.info('Total unique_asins_to_parse: %s', len(unique_asins_to_parse))

        # Load rating and reviews
        amazon_request_sender = AmazonZenRowsRequestSender()
        product_collector = AmazonProductCollector(
            product_convertor=AmazonProductConverter(),
            # product_page_provider=AmazonProductPageProvider(amazon_request_sender=amazon_request_sender),
            product_page_provider=AmazonProductPageFileReader(products_dir=AMAZON_PRODUCT_PAGES_DIR),  # TEST
        )
        product_collector_use_case = CollectAmazonProductsUseCase(
            product_collector=product_collector,
        )
        products_from_pars = product_collector_use_case.collect(items=unique_asins_to_parse)
        logging.info('Total parsed asins: %s', len(products_from_pars))

        # Join data from reports with data from pars
        for product in active_products:
            for product_from_pars in products_from_pars:
                if product.asin == product_from_pars.asin and \
                        product.marketplace_country.value == product_from_pars.marketplace_country:
                    product.rating = product_from_pars.rating
                    product.rating_reviews = product_from_pars.rating_reviews
                    break

        # Send data to airtable
        update_products_use_case = UpdateAmazonProductsTableUseCase(
            product_sender=AirTableProductSender(),
        )
        update_products_use_case.update_table(products=active_products)
        logging.info('\nEnd')
