from aiogram import types
from crud.users import GroupCRUD
from enums.languages import LanguageEnum
from schemas.users import GroupUpdateSchema
from services.chats import ChatService
from telegram.dispatcher import dp


@dp.message_handler(commands=["setlang"])
async def set_language(message: types.Message):
    """Set language to user, group"""

    lang = message.get_args().split()
    available_languages = [l.value for l in LanguageEnum]
    if not lang:
        text = "*Available languages:*\n"
        text += "\n".join(available_languages)
        await ChatService.reply(message, text, is_markdown=True)
        return
    if len(lang) > 1:
        await ChatService.reply(message, "Wrong usage\. Example: `/setlang ru`", is_markdown=True)
        return

    lang, = lang
    if lang not in available_languages:
        await ChatService.reply(message, "This language not available yet. You can suggest more language support")
        return

    if ChatService.is_group(message.chat):
        await GroupCRUD.update_group(telegram_id=message.chat.id, data=GroupUpdateSchema(language=lang))
        await ChatService.reply(message, f"Language set: {lang}")
        return
