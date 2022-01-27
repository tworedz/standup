from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from telegram.bot import bot

dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
Bot.set_current(dp.bot)
Dispatcher.set_current(dp)
