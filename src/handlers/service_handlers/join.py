from aiogram import types

from crud.films import FilmCRUD
from crud.users import GroupCRUD
from schemas.films import FilmSettingUpdateOrCreateSchema
from schemas.users import GroupCreateSchema
from services.chats import ChatService
from telegram.dispatcher import dp


@dp.my_chat_member_handler()
async def bot_joined_to_chat(update: types.ChatMemberUpdated) -> None:
    """ """

    if ChatService.is_group(update.chat):
        await GroupCRUD.update_or_create_group(
            group_data=GroupCreateSchema(telegram_id=update.chat.id, title=update.chat.title)
        )

    if ChatService.is_channel(update.chat):
        await FilmCRUD.update_or_create_channel_settings(
            telegram_channel_id=update.chat.id,
            data=FilmSettingUpdateOrCreateSchema(),
        )

    await update.bot.send_message(update.chat.id, "Hello, friends!")
