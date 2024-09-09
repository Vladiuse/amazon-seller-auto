class ReportCreationError(Exception):
    """throw if report not created"""


class ReportDocumentNotComplete(Exception):
    """Trow if report document status not in []"""


class ReportStatusError(Exception):
    """Throw if report processing status is FATAL or CANCELED"""
