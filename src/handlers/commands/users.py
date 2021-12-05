from typing import Tuple

import aiogram
from aiogram import types
import asyncio

from core.logging import logger
from crud.users import UserCRUD
from schemas.users import UserSchema
from telegram.bot import bot
from telegram.dispatcher import dp


def get_tag(text: str, entity: types.MessageEntity) -> Tuple[str, int]:
    if entity.type == types.MessageEntityType.MENTION:
        return text[entity.offset: entity.offset + entity.length], 0
    elif entity.type == types.MessageEntityType.TEXT_MENTION:
        return entity.user.username, entity.user.id


@dp.message_handler(commands=["register"])
async def register_user(message: types.Message) -> None:
    mentions = message.entities[1:]
    if not mentions:
        response = await message.reply(
            "Wrong command. Usage: `/register @durov`",
            parse_mode=types.ParseMode.HTML,
        )
        await asyncio.sleep(3)
        await message.delete()
        await response.delete()
        return

    user_tags = [
        get_tag(message.text, entity) for entity in mentions
    ]

    for user_name, user_id in user_tags:
        await UserCRUD.create_user(
            user=UserSchema(id=user_id, username=user_name)
        )
    response = await message.reply("Users added!")

    await asyncio.sleep(5)
    try:
        await response.delete()
        await message.delete()
    except aiogram.exceptions.MessageToDeleteNotFound:
        logger.warning("Messages not found")


@dp.message_handler(commands=["users"])
async def get_users(message: types.Message) -> None:
    users = await UserCRUD.get_users()
    users = [user.username for user in users]
    response = await message.reply(",".join(users))
    await asyncio.sleep(3)
    await message.delete()
    await response.delete()
