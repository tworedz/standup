from typing import Tuple

import aiogram
from aiogram import types
import asyncio

from core.logging import logger
from crud.users import UserCRUD
from schemas.users import UserSchema, UserCreateSchema
from telegram.bot import bot
from telegram.dispatcher import dp


@dp.message_handler(commands=["start"])
async def register_user(message: types.Message) -> None:
    user = message.from_user
    chat = message.chat

    await UserCRUD.get_or_create_user(
        user_data=UserCreateSchema(
            username=user.username,
            telegram_id=user.id,
            name=user.first_name,
            surname=user.last_name,
        )
    )
    await asyncio.sleep(3)
    await message.delete()


@dp.message_handler(commands=["users"])
async def get_users(message: types.Message) -> None:
    users = await UserCRUD.get_users()
    users = [user.dict() for user in users]
    response = await message.reply("\n".join(map(str, users)))
    await asyncio.sleep(10)
    await message.delete()
    await response.delete()
