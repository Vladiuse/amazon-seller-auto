from typing import Annotated

from pydantic import BaseModel, StringConstraints


class Asin(BaseModel):
    value: Annotated[str, StringConstraints(max_length=10, min_length=10, to_upper=True)]
