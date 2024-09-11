class ReportDocumentNotComplete(Exception):
    """Trow if report document status not in []"""


class ReportStatusError(Exception):
    """Throw if report processing status is FATAL or CANCELED"""

class MaxTriesError(Exception):
    """Throw if @retry attempts exceed"""

class ParserError(Exception):
    """Throw if some data not found in html"""

class HtmlElementNotFound(ParserError):
    """Throw if html element not found"""

