from datetime import datetime

from pydantic import BaseModel, Field
from sp_api.base import ProcessingStatus, ReportType


class AmazonReport(BaseModel):
    report_id: str = Field(alias='reportId')
    marketplace_ids: list[str] = Field(alias='marketplaceIds')
    processing_status: ProcessingStatus = Field(alias='processingStatus')
    report_type: ReportType = Field(alias='reportType')
    created: datetime = Field(alias='createdTime')
    document_id: str | None = Field(default=None, alias='reportDocumentId')

    def is_complete(self) -> bool:
        return self.processing_status in [ProcessingStatus.DONE, ProcessingStatus.FATAL,
                                          ProcessingStatus.CANCELLED]

    def is_document_created(self) -> bool:
        return self.processing_status == ProcessingStatus.DONE


class ReportDocument(BaseModel):
    id: str = Field(alias='reportDocumentId')
    url: str
