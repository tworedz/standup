import logging

from pydantic import AnyHttpUrl
from pydantic import BaseSettings
from pydantic import SecretStr
from pydantic import validator


class Settings(BaseSettings):
    """Project settings from env variables"""

    APP_DEBUG: bool = True
    DEBUG_LEVEl: str = logging.getLevelName(logging.DEBUG)
    HOST_PATH: AnyHttpUrl
    DATABASE_CLASS: str = "db.database.MemoryDatabase"
    WEBHOOK_ENABLED: bool = False

    # Telegram
    TELEGRAM_BOT_API_KEY: SecretStr
    TELEGRAM_BOT_WEBHOOK_ENDPOINT: str = ""
    TELEGRAM_DROP_PENDING_UPDATES: bool = True

    @validator("TELEGRAM_BOT_WEBHOOK_ENDPOINT")
    def construct_webhook(cls, v, values: dict) -> str:
        return (
            values.get("HOST_PATH")
            + "telegram/webhook/"
            + values.get("TELEGRAM_BOT_API_KEY").get_secret_value()
            + "/"
        )


settings = Settings()
