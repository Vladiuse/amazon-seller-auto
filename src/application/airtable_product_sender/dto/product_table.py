from enum import Enum
from typing import Any

from pyairtable.orm import Model
from pyairtable.orm import fields as F
from pydantic import BaseModel

from src.main.amazonconfig import airtable_config


class AirTableFieldType(Enum):
    SINGLE_LINE_TEXT = 'singleLineText'
    NUMBER = 'number'


class AirTableField(BaseModel):
    name: str
    type: AirTableFieldType
    description: str | None = None
    options: dict[str, Any] | None = None


class TextField(AirTableField):
    type: AirTableFieldType = AirTableFieldType.SINGLE_LINE_TEXT


class NumberField(AirTableField):
    type: AirTableFieldType = AirTableFieldType.NUMBER
    options: dict[str, Any]


class AirTableRequest(BaseModel):
    name: str
    description: str | None = None
    fields: list[AirTableField]


CREATE_AMAZON_PRODUCT_TABLE_DATA = AirTableRequest(
    name='Amazon products',
    description='created by api',
    fields=[
        TextField(name='asin'),
        TextField(name='sku'),
        TextField(name='name'),
        TextField(name='marketplace_country'),
        NumberField(name='available', options={'precision': 0}),
        NumberField(name='inbound', options={'precision': 0}),
        TextField(name='featured_offer'),
        NumberField(name='inbound_receiving_qty', options={'precision': 0}),
        NumberField(name='rating', options={'precision': 2}),
        NumberField(name='rating_reviews', options={'precision': 0}),
    ],
)


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

    class Meta:
        base_id = airtable_config.AIRTABLE_APP_ID
        table_name = "tblzufSUwmXFyRQon"
        api_key = airtable_config.AIRTABLE_API_KEY
