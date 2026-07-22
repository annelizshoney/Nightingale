from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    API_PREFIX: str
    LOG_LEVEL: str

    # Database
    DATABASE_URL: str

    # Authentication
    SECRET_KEY: str
    JWT_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()