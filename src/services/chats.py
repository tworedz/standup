from typing import Union
from aiogram.utils import exceptions

from aiogram import types

from core.logging import logger
from sdk.utils import wait_for


class ChatService:
    @classmethod
    def is_group(cls, chat: types.Chat) -> bool:
        return chat.type in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]

    @classmethod
    async def reply(
        cls,
        message: types.Message,
        text: str,
        reply_markup: Union[
            types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply,
            None,
        ] = None,
        /,
        delete: bool = True,
        is_markdown: bool = False,
    ) -> None:
        """Reply to message
        This conversation may be deleted, if `delete` is True and bot has permissions
        """

        parse_mode = types.ParseMode.MARKDOWN_V2 if is_markdown else None
        response = await message.reply(
            text=text, parse_mode=parse_mode, reply_markup=reply_markup
        )
        if delete:
            await wait_for()
            try:
                await response.delete()
                await message.delete()
            except exceptions.MessageCantBeDeleted as e:
                logger.debug("Cannot remove messages", error=e)
