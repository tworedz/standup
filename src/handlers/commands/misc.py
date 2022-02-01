import asyncio
import random

from aiogram import types

from crud.feedbacks import FeedbackCRUD
from schemas.feedbacks import FeedbackCreateSchema
from sdk.utils import wait_for
from services.chats import ChatService
from telegram import messages
from telegram.dispatcher import dp


@dp.message_handler(commands=["ping"])
async def ping(message: types.Message):
    """Ping!"""

    await ChatService.reply(message, "Pong!")


@dp.message_handler(commands=["feedback"])
async def feedback_handler(message: types.Message) -> None:
    """Feedback from user"""

    args = message.get_args()
    if not args:
        await ChatService.reply(message, "Example: `/feedback Add language support`")

    await FeedbackCRUD.create_feedback(
        data=FeedbackCreateSchema(from_user_telegram_id=message.from_user.id, message=args)
    )
    await ChatService.reply(message, messages.THANKS_FOR_FEEDBACK)
