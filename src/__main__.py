from csv import DictWriter
from itertools import product

from sp_api.base import Marketplaces, ReportType

from src.adapters.amazon_products_collector import AmazonReportProductsCollector
from src.adapters.amazon_reports_collector import AmazonReportCollector
from src.adapters.amazon_report_product_convertor import ReportProductConvertor
from sp_api.base.exceptions import SellingApiException
from src.main.exceptions import ReportCreationError
from src.adapters.amazon_products_collector import AmazonReportProductsCollector
from src.adapters.amazon_reports_collector import AmazonReportCollector
from src.adapters.amazon_report_product_convertor import ReportProductConvertor
from src.application.amazon_product_collector.dto.product import AmazonReportProduct
import csv
# GET_FBA_MYI_ALL_INVENTORY_DATA inventory
# GET_REFERRAL_FEE_PREVIEW_REPORT 403 forbined
# GET_FBA_STORAGE_FEE_CHARGES_DATA calceled
# GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA  есть нужный параметр но не полный список позиций
ACTIVE_IDS = [
    'B09GFLXSRF'
    'B09W1GZMR1',
    'B0BQMSMZJ3',
    'B09GFQQ1CM',
    'B0BK1DZGND',
    'B0BK1KDS19',
    'B09R1YR2V2',
    'B09YCZ3VYV',
    'B09HVCKFTB',
    'B091CYLSNF',
    'B0BK196QNQ',
    'B0BK1572HN',
    'B0B5GN86QG',
    'B0BJZZCVQ1',
    'B0BJZYJTVX',
    'B0CLRR1WWK',
    'B0BK9NP2XP',
    'B0BK9Q8G2T',
    'B0CBQ9FMLL',
    'B0CBQCHTJ9',
]

marketplaces = [
    Marketplaces.IT,
    Marketplaces.FR,
    Marketplaces.ES,
    Marketplaces.DE,
    Marketplaces.GB,
]
report_type = ReportType.GET_FBA_MYI_ALL_INVENTORY_DATA

products = []
collector = AmazonReportProductsCollector(
    report_collector= AmazonReportCollector,
    report_convertor= ReportProductConvertor,
)
# for marketplace in marketplaces:
#     print(marketplace)
#     report_products = collector.collect(report_type=report_type, marketplace=marketplace)
#     products.extend(report_products)
#
# with open('x.csv', 'w') as file:
#     fieldnames = list[AmazonReportProduct.model_fields]
#     writer = DictWriter(file, delimiter=',', quotechar='"', fieldnames=fieldnames)
#     writer.writeheader()
#     for i in products:
#         writer.writerow(i.model_dump())

collector = AmazonReportCollector(marketplace=Marketplaces.IT)
collector.get_report(report_id='1147563019975')