from pyairtable.orm import Model
from pyairtable.orm import fields as F

from src.main.config import config


class AmazonProductTable(Model):
    asin = F.TextField("asin")
    sku = F.TextField("sku")
    name = F.TextField("name")
    marketplace_country = F.TextField("marketplace_country")
    available = F.NumberField("available")
    inbound = F.NumberField("inbound")
    featured_offer = F.TextField("featured_offer")
    inbound_receiving_qty = F.NumberField("inbound_receiving_qty")
    rating = F.NumberField("rating")
    rating_reviews = F.NumberField("rating_reviews")
    units_ordered = F.NumberField("units_ordered")
    fba_fee = F.NumberField("fba_fee")
    fc_transfer = F.NumberField("fc_transfer")

    class Meta:
        base_id = config.airtable_config.AIRTABLE_APP_ID
        table_name = config.airtable_config.AIRTABLE_MAIN_TABLE_ID
        api_key = config.airtable_config.AIRTABLE_API_KEY


class AmazonVendorSalesTable(Model):
    asin = F.TextField("asin")
    marketplace_country = F.TextField("marketplace_country")
    ordered_units = F.NumberField("ordered_units")

    class Meta:
        base_id = config.airtable_config.AIRTABLE_APP_ID
        table_name = config.airtable_config.AIRTABLE_VENDOR_SALES_TABLE_ID
        api_key = config.airtable_config.AIRTABLE_API_KEY
