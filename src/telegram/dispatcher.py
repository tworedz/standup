from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from core.config import settings
from sdk.middlewares import AuthenticationMiddleware
from telegram.bot import bot

dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(AuthenticationMiddleware(settings.TELEGRAM_ALLOWED_COMMANDS))
Bot.set_current(dp.bot)
Dispatcher.set_current(dp)
