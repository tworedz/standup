import logging
from typing import Optional

from enums.languages import LanguageEnum
from pydantic import AnyHttpUrl
from pydantic import BaseSettings
from pydantic import PostgresDsn
from pydantic import SecretStr
from pydantic import validator


class Settings(BaseSettings):
    """Project settings from env variables"""

    APP_DEBUG: bool = True
    DEBUG_LEVEl: str = logging.getLevelName(logging.INFO)
    HOST_PATH: AnyHttpUrl = "http://localhost"
    WEBHOOK_ENABLED: bool = False
    TS_SITE: str = "https://www.cinematica.kg/movies/"

    # Telegram
    MY_USERNAME: str = ""
    TELEGRAM_BOT_API_KEY: SecretStr = ""
    TELEGRAM_BOT_WEBHOOK_ENDPOINT: str = ""
    TELEGRAM_DROP_PENDING_UPDATES: bool = True
    TELEGRAM_ALLOWED_COMMANDS: list[str] = [
        "start",
        "help",
        "ping",
        "feedback",
    ]

    @validator("TELEGRAM_BOT_WEBHOOK_ENDPOINT")
    def construct_webhook(cls, v, values: dict) -> str:
        return (
            values.get("HOST_PATH")
            + "telegram/webhook/"
            + values.get("TELEGRAM_BOT_API_KEY").get_secret_value()
            + "/"
        )

    # Database settings
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "breez_bot"
    DB_URI: Optional[PostgresDsn] = None

    @validator("DB_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=str(values.get("DB_PORT")),
            path=f"/{values.get('DB_NAME')}",
        )


settings = Settings()
