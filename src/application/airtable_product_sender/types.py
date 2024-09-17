from dataclasses import dataclass
from enum import Enum
from typing import Any


class AirTableFieldType(Enum):
    SINGLE_LINE_TEXT = 'singleLineText'
    NUMBER = 'number'


@dataclass
class AirTableField:
    name: str
    type: AirTableFieldType
    description: str | None = None
    options: dict[str, Any] | None = None
