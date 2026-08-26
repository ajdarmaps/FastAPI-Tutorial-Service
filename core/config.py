from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from typing import Literal


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    APP_ENV: Literal[
        "development",
        "testing",
        "production",
    ] = "development"
    DEBUG: bool = False
    LOG_LEVEL: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.APP_ENV == "production" and self.DEBUG:
            raise ValueError("DEBUG must be false when APP_ENV is production")

        return self


settings = Settings()
