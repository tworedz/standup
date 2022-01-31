import asyncio

import aiogram
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


class AuthenticationMiddleware(BaseMiddleware):
    """Проверка прав пользователя"""

    def __init__(self, allowed_commands: list[str]) -> None:
        self.allowed_commands = allowed_commands
        super().__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        if not message.is_command():
            return

        command = message.get_command(pure=True)
        current_user = message.from_user
        administrators = await message.chat.get_administrators()
        admin_ids = [admin.user.id for admin in administrators]
        if current_user.id not in admin_ids and command not in self.allowed_commands:
            response = await message.reply("This command only allowed to administrators")
            await asyncio.sleep(5)
            try:
                await message.delete()
                await response.delete()
            except (aiogram.exceptions.MessageCantBeDeleted, aiogram.exceptions.MessageToDeleteNotFound):
                pass
            raise CancelHandler()
