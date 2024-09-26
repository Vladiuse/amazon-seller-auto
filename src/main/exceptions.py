class ApplicationException(Exception):
    """ApplicationException"""


class ReportDocumentNotComplete(ApplicationException):
    """Trow if report document status not in []"""


class ReportStatusError(ApplicationException):
    """Throw if report processing status is FATAL or CANCELED"""


class MaxTriesError(ApplicationException):
    """Throw if @retry attempts exceed"""


class ParserError(ApplicationException):
    """Throw if some data not found in html"""


class HtmlElementNotFound(ParserError):
    """Throw if html element not found"""
