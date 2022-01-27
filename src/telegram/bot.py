from aiogram import Bot
from core.config import settings

bot = Bot(token=settings.TELEGRAM_BOT_API_KEY.get_secret_value())
