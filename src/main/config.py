from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    SP_API_REFRESH_TOKEN: str
    LWA_APP_ID: str
    LWA_CLIENT_SECRET: str
    LWA_CLIENT_ID: str
    ENV_DISABLE_DONATION_MSG: int


class AirTableConfig(BaseSettings):
    AIRTABLE_API_KEY: str
    AIRTABLE_APP_ID: str


config = Config()
airtable_config = AirTableConfig()

credentials = {
    'refresh_token': config.SP_API_REFRESH_TOKEN,
    'lwa_app_id': config.LWA_CLIENT_ID,
    'lwa_client_secret': config.LWA_CLIENT_SECRET,
}
