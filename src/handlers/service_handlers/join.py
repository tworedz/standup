from aiogram import types

from crud.users import GroupCRUD
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
    await update.bot.send_message(
        update.chat.id, f"Hello, friends!"
    )
