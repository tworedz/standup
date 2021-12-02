from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.telegram.bot import bot

dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
