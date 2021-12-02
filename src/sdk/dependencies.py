from aiogram import Bot
from aiogram import Dispatcher
from fastapi_security_telegram_webhook import OnlyTelegramNetworkWithSecret


from src.core.config import settings
from src.telegram.dispatcher import dp


def bot_dispatcher() -> Dispatcher:
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)
    return dp


def telegram_bot() -> Bot:
    return dp.bot


telegram_webhook_security = OnlyTelegramNetworkWithSecret(
    real_secret=settings.TELEGRAM_BOT_WEBHOOK_SECRET.get_secret_value()
)
