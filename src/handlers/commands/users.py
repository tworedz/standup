import asyncio
from typing import Tuple

import aiogram
from aiogram import types
from core.logging import logger
from crud.users import GroupCRUD
from crud.users import UserCRUD
from schemas.users import GroupCreateSchema
from schemas.users import UserCreateSchema
from schemas.users import UserSchema
from sdk.utils import wait_for
from services.chats import ChatService
from telegram.bot import bot
from telegram.dispatcher import dp


@dp.message_handler(aiogram.dispatcher.filters.CommandStart())
async def register_user(message: types.Message) -> None:
    telegram_user = message.from_user
    chat = message.chat

    user = await UserCRUD.get_user(telegram_user.id)
    if user:
        user = await UserCRUD.update_user(
            user_data=UserCreateSchema(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                name=telegram_user.first_name,
                surname=telegram_user.last_name,
                mention=telegram_user.get_mention(),
            )
        )
    else:
        user = await UserCRUD.create_user(
            user_data=UserCreateSchema(
                username=telegram_user.username,
                telegram_id=telegram_user.id,
                name=telegram_user.first_name,
                surname=telegram_user.last_name,
                mention=telegram_user.get_mention(),
            )
        )

    if chat.type in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]:
        group = await GroupCRUD.get_or_create_group(
            group_data=GroupCreateSchema(telegram_id=chat.id, title=chat.title)
        )
        await GroupCRUD.add_user_to_group(user_id=user.id, group_id=group.id)

    reply = await message.reply(
        text=f"Welcome to the club, {telegram_user.get_mention()}",
        parse_mode=types.ParseMode.MARKDOWN_V2,
    )
    await wait_for()
    if ChatService.is_group(chat):
        await message.delete()
        await reply.delete()


@dp.message_handler(commands=["users"])
async def get_users(message: types.Message) -> None:
    chat = message.chat
    if chat.type == types.ChatType.PRIVATE:
        return

    users = await UserCRUD.get_users()
    users = [f"{user.mention}" for user in users]
    response = await message.reply("\n".join(map(str, users)), parse_mode=types.ParseMode.MARKDOWN_V2)
    await wait_for()
    await message.delete()
    await response.delete()


@dp.message_handler(commands=["register"])
async def register_user(message: types.Message) -> None:
    if message.chat.type not in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]:
        await message.reply("This command used only in groups")
        return

    mentions = message.entities[1:]
    if not mentions:
        response = await message.reply(
            "Wrong command. Usage: `/register @durov`",
            parse_mode=types.ParseMode.MARKDOWN_V2,
        )
        await asyncio.sleep(3)
        await message.delete()
        await response.delete()
        return
