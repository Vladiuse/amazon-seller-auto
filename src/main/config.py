from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

ACTIVE_ASINS_FILE_PATH = 'active_asins.txt'
REPORTS_DIR = 'media/reports/'
AMAZON_PRODUCT_PAGES_DIR = 'media/zen_pars'


class AmazonConfig(BaseSettings):
    SP_API_REFRESH_TOKEN: str
    LWA_APP_ID: str
    LWA_CLIENT_SECRET: str
    LWA_CLIENT_ID: str
    ENV_DISABLE_DONATION_MSG: int


class AirTableConfig(BaseSettings):
    AIRTABLE_API_KEY: str
    AIRTABLE_APP_ID: str
    AIRTABLE_TABLE_ID: str


class ZenRowConfig(BaseSettings):
    ZENROWS_API_KEY: str


class Config(BaseSettings):
    amazon_config = AmazonConfig()
    airtable_config = AirTableConfig()
    zenrows_config = ZenRowConfig()


config = Config()
