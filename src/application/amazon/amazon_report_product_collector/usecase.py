import requests
from requests.exceptions import RequestException

from src.application.amazon.utils import retry


class GetAmazonReportDocumentTextUseCase:

    @retry(
        attempts=5,
        delay=10,
        exceptions=(RequestException,),
    )
    def get_text(self, report_document_url: str) -> str:
        response = requests.get(report_document_url)
        response.raise_for_status()
        return response.text
