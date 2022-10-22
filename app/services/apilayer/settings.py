from pydantic import AnyHttpUrl, BaseSettings, validator


class ApiLayerSettings(BaseSettings):
    APILAYER_API_KEY: str
    APILAYER_CONNECTION_TIMEOUT: str = '30 secs'

    class Config:
        case_sensitive = False
        env_file = '.env'
