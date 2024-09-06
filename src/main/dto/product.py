import csv
import os
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass

from pydantic import BaseModel, Field

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


class MarketplaceCountry(str, Enum):
    FR = 'FR'
    IT = 'IT'
    DE = 'DE'
    GB = 'GB'
    ES = 'ES'


asin = str


class AmazonProduct(BaseModel):
    asin: asin
    name: str = Field(alias='product-name')
    marketplace_country: MarketplaceCountry
    sku: str
    available: int = Field(alias='afn-fulfillable-quantity')
    inbound: int = Field(alias='afn-inbound-shipped-quantity')
    featured_offer: str = Field(alias='your-price')
    inbound_receiving_qty: int = Field(alias='afn-inbound-receiving-quantity')
    rating: float | None = None
    rating_reviews: int | None = None


class AmazonProductRepository:

    @abstractmethod
    def get_all_products(self, *args, **kwargs) -> list[AmazonProduct]:
        raise NotImplementedError

@dataclass(frozen=True)
class IGetAllProductsUseCase(ABC):
    product_repository: AmazonProductRepository

    @abstractmethod
    def __call__(self) -> list[AmazonProduct]:
        raise NotImplementedError

@dataclass(frozen=True)
class GetAllProductsUseCase(IGetAllProductsUseCase):

    def __call__(self) -> list[AmazonProduct]:
        return self.product_repository.get_all_products()


class InReportProductRepository(AmazonProductRepository):

    def get_all_products(self) -> list[AmazonProduct]:
        reports_dir_path = '/home/vlad/PycharmProjects/amazon-seller-auto/media/reports'
        products = []
        for file_name in os.listdir(reports_dir_path):
            path = os.path.join(reports_dir_path, file_name)
            marketplace_country = file_name[:2]
            if os.path.isfile(path):
                print(path)
                with open(path) as file:
                    reader = csv.DictReader(file, delimiter='\t')
                    for row in reader:
                        product = AmazonProduct(marketplace_country=marketplace_country, **row)
                        products.append(product)
        return products


def get():
    get_all_products_use_case = GetAllProductsUseCase(
        product_repository=InReportProductRepository(),
    )

    return get_all_products_use_case()


print(get())

# with open('/home/vlad/JOIN.csv', 'w') as csv_file:
#     fields = list(AmazonProductDailyReportStat.model_fields.keys())
#     writer = csv.DictWriter(csv_file, delimiter=',', fieldnames=fields)
#     writer.writeheader()
#     for product in products:
#         if product.asin in ACTIVE_IDS:
#             print(product.model_dump())
#             writer.writerow(product.model_dump())
