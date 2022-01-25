import asyncio

from aiogram import types
import random
from telegram.dispatcher import dp


@dp.message_handler(commands=["ping"])
async def ping(message: types.Message):
    """Ping!"""

    answer = await message.answer("Pong!")
    await asyncio.sleep(5)
    await answer.delete()
    await message.delete()


@dp.message_handler(commands=["random"])
async def random_handler(message: types.Message) -> None:
    """Sends random"""

    emojies = [
        "🎲",
        "🎯",
        "🏀",
        "⚽",
        "🎰",
    ]
    response = await message.answer_dice(emoji=random.choice(emojies), reply=True)
    await asyncio.sleep(3)
    r = await response.answer(
        f"Your random for {response.dice.emoji} is {response.dice.value}"
    )
    await asyncio.sleep(5)
    await message.delete()
    await response.delete()
    await r.delete()


@dp.message_handler(content_types=types.ContentTypes.DICE)
async def dice(message: types.Message):
    """Echo to message"""

    await message.reply(message.dice.value)


# @dp.message_handler(content_types=types.ContentTypes.ANY)
# async def all_the_messages(message: types.Message):
#     """All the messages"""
#
#     print(message)
