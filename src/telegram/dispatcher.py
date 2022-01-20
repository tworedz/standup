from aiogram import Dispatcher, Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from telegram.bot import bot

dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
Bot.set_current(dp.bot)
Dispatcher.set_current(dp)
