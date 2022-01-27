import asyncio
import random

from aiogram import types
from sdk.utils import wait_for
from telegram.dispatcher import dp


@dp.message_handler(commands=["ping"])
async def ping(message: types.Message):
    """Ping!"""

    answer = await message.answer("Pong!")
    await wait_for()
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
    await asyncio.sleep(4)
    r = await response.answer(f"Your random for {response.dice.emoji} is {response.dice.value}")
    await wait_for()
    await message.delete()
    await response.delete()
    await r.delete()
