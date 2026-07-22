from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Nightingale"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()