import asyncio
import random

from aiogram import types

from crud.feedbacks import FeedbackCRUD
from schemas.feedbacks import FeedbackCreateSchema
from sdk.utils import wait_for
from telegram import messages
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


@dp.message_handler(commands=["feedback"])
async def feedback_handler(message: types.Message) -> None:
    """Feedback from user"""

    args = message.get_args()
    if not args:
        response = await message.reply(
            "Example: `/feedback Add language support`", parse_mode=types.ParseMode.MARKDOWN_V2
        )
        await wait_for()
        await message.delete()
        await response.delete()
        return

    await FeedbackCRUD.create_feedback(
        data=FeedbackCreateSchema(from_user_telegram_id=message.from_user.id, message=args)
    )
    response = await message.reply(messages.THANKS_FOR_FEEDBACK)
    await wait_for()
    await message.delete()
    await response.delete()
