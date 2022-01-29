from aiogram import types


class ChatService:
    @classmethod
    def is_group(cls, chat: types.Chat) -> bool:
        return chat.type in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]
