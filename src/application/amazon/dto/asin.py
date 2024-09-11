from typing import Annotated

from pydantic import BaseModel, StringConstraints

AsinStr = Annotated[str, StringConstraints(max_length=10, min_length=10, to_upper=True)]

class Asin(BaseModel):
    value: AsinStr
