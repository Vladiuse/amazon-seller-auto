from pydantic import BaseModel

from src.application.airtable_product_sender.types import AirTableField


class AirTableRequest(BaseModel):
    name: str
    description: str | None = None
    fields: list[AirTableField]
