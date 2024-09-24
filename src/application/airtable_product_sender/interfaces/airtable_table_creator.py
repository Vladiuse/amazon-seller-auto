from abc import ABC, abstractmethod

from src.application.airtable_product_sender.dto.table_records import AirTableCreateRequest


class IAirtableTableCreator(ABC):

    @abstractmethod
    def create_table(self, table_request: AirTableCreateRequest) -> None:
        raise NotImplementedError
