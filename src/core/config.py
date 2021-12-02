from pydantic import AnyHttpUrl
from pydantic import BaseSettings
from pydantic import SecretStr
from pydantic import validator


class Settings(BaseSettings):
    """Project settings from env variables"""

    TELEGRAM_BOT_API_KEY: SecretStr
    TELEGRAM_BOT_WEBHOOK_SECRET: SecretStr = ""
    HOST_PATH: AnyHttpUrl
    TELEGRAM_BOT_WEBHOOK_ENDPOINT: str = ""

    @validator("TELEGRAM_BOT_WEBHOOK_ENDPOINT")
    def construct_webhook(cls, v, values: dict) -> str:
        return (
            values.get("HOST_PATH")
            + "telegram/webhook/"
            + values.get("TELEGRAM_BOT_WEBHOOK_SECRET")
        )


settings = Settings()
