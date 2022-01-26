from typing import Tuple

import aiogram
from aiogram import types
import asyncio

from core.logging import logger
from crud.users import UserCRUD, GroupCRUD
from schemas.users import UserSchema, UserCreateSchema, GroupCreateSchema
from telegram.bot import bot
from telegram.dispatcher import dp


def get_tag(text: str, entity: types.MessageEntity) -> Tuple[str, int]:
    if entity.type == types.MessageEntityType.MENTION:
        return text[entity.offset : entity.offset + entity.length], 0
    elif entity.type == types.MessageEntityType.TEXT_MENTION:
        return entity.user.full_name, entity.user.id


@dp.message_handler(aiogram.dispatcher.filters.CommandStart())
async def register_user(message: types.Message) -> None:
    telegram_user = message.from_user
    chat = message.chat

    group = await GroupCRUD.get_or_create_group(group_data=GroupCreateSchema(telegram_id=chat.id, title=chat.title))
    user = await UserCRUD.get_or_create_user(
        user_data=UserCreateSchema(
            username=telegram_user.username,
            telegram_id=telegram_user.id,
            name=telegram_user.first_name,
            surname=telegram_user.last_name,
        )
    )
    await GroupCRUD.add_user_to_group(user_id=user.id, group_id=group.id)

    reply = await message.answer_animation(
        caption=f"Welcome to the club, {telegram_user.get_mention()}",
        animation="CgACAgQAAxkBAAIE7GHvi8d_Y_sUOv4EuezxkMV1iRmBAAKuoAACrhtkB-N_sxcPEI_5IwQ",
        parse_mode=types.ParseMode.MARKDOWN_V2,
    )
    await asyncio.sleep(5)
    if chat.type == types.chat.ChatType.GROUP:
        await message.delete()
        await reply.delete()


@dp.chat_member_handler()
async def member_join(chat_member: types.ChatMemberUpdated) -> None:
    print(chat_member, chat_member.user)


@dp.message_handler(commands=["users"])
async def get_users(message: types.Message) -> None:
    users = await UserCRUD.get_users()
    users = [f"{user.username} ({user.telegram_id})" for user in users]
    response = await message.reply("\n".join(map(str, users)))
    await asyncio.sleep(5)
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

    user_tags = [get_tag(message.text, entity) for entity in mentions]
