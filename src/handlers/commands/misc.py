from aiogram import types
import random
from telegram.dispatcher import dp


@dp.message_handler(commands=["ping"])
async def ping(message: types.Message):
    """Ping!"""

    await message.answer("Pong!")


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
    await response.answer(
        f"Your random for {response.dice.emoji} is {response.dice.value}"
    )


@dp.message_handler(content_types=types.ContentTypes.DICE)
async def dice(message: types.Message):
    """Echo to message"""

    await message.reply(message.dice.value)
