from aiogram import Bot
from aiogram import Dispatcher
from telegram.dispatcher import dp


def bot_dispatcher() -> Dispatcher:
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)
    return dp


def telegram_bot() -> Bot:
    return dp.bot
