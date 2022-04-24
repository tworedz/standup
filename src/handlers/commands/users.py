import aiogram
from aiogram import types
from crud.users import GroupCRUD
from crud.users import UserCRUD
from schemas.users import GroupCreateSchema
from schemas.users import UserCreateSchema
from schemas.users import UserUpdateSchema
from sdk.utils import wait_for
from services.chats import ChatService
from telegram.dispatcher import dp


@dp.message_handler(aiogram.dispatcher.filters.CommandStart())
async def start_command(message: types.Message) -> None:
    telegram_user = message.from_user
    chat = message.chat

    user = await UserCRUD.get_user_by_telegram_id(telegram_user.id)
    if user:
        user = await UserCRUD.update_user(
            telegram_id=telegram_user.id,
            user_data=UserUpdateSchema(
                username=telegram_user.username,
                name=telegram_user.first_name,
                surname=telegram_user.last_name,
                mention=telegram_user.get_mention(),
            ),
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

    if ChatService.is_group(chat):
        group = await GroupCRUD.update_or_create_group(
            group_data=GroupCreateSchema(telegram_id=chat.id, title=chat.title)
        )
        await GroupCRUD.add_user_to_group(user_id=user.id, group_id=group.id)

    await ChatService.reply(
        message, f"Welcome to the club, {telegram_user.get_mention()}", is_markdown=True
    )


@dp.message_handler(commands=["users"])
async def get_users(message: types.Message) -> None:
    chat = message.chat
    if chat.type == types.ChatType.PRIVATE:
        return

    users = await UserCRUD.get_group_users(telegram_id=chat.id)
    if not users:
        await ChatService.reply(message, "No one joined to this group(")
        return

    users = [f"{user.mention}" for user in users]
    await ChatService.reply(message, "\n".join(map(str, users)), is_markdown=True)
