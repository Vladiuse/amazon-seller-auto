
from sp_api.base import Marketplaces

from src.main.reports import create_report, download_report

marketplace = Marketplaces.IT
report_id = create_report(marketplace=marketplace)
download_report(report_id=report_id, marketplace=marketplace)
