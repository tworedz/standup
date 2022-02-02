import asyncio
import random

from aiogram import types

from core.config import settings
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
        await ChatService.reply(message, "Example: `/feedback Add language support`", is_markdown=True)
        return

    await FeedbackCRUD.create_feedback(
        data=FeedbackCreateSchema(from_user_telegram_id=message.from_user.id, message=args)
    )
    await ChatService.reply(message, messages.THANKS_FOR_FEEDBACK)


@dp.message_handler(commands=["gaf"])
async def get_all_feedbacks(message: types.Message) -> None:
    """All the feedbacks"""

    if message.chat.type != types.ChatType.PRIVATE:
        return

    if message.from_user.username != settings.MY_USERNAME:
        return

    feedbacks = await FeedbackCRUD.get_feedbacks()
    if not feedbacks:
        text = "No one send feedback"
    else:
        text = "\n".join([feedback.message for feedback in feedbacks])

    await ChatService.reply(message, text=text)
