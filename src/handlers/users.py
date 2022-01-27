from aiogram import types
from telegram.dispatcher import dp


@dp.message_handler(commands=["add_user"])
async def add_user(message: types.Message) -> None:
    await message.reply(message.get_args())
