from uuid import UUID

import aiogram.types.inline_keyboard
from aiogram import types
from aiogram import filters
from core.logging import logger
from crud.users import UserCRUD
from crud.warmups import WarmUpSummonCRUD
from services.warmups import WarmUpSummonService
from telegram import messages
from telegram.dispatcher import dp


@dp.callback_query_handler(filters.Regexp(regexp=r"remove_summoner_.*?"))
async def remove_summoner_handler(callback_query: types.CallbackQuery) -> None:
    summoner_id = UUID(callback_query.data.replace("remove_summoner_", ""))
    try:
        await WarmUpSummonCRUD.delete_summoner(summoner_id)
    except Exception as e:
        logger.warning("Summoner not found", error=e)
        return

    txt, keyboard = await WarmUpSummonService.get_summoners_list_data()
    await callback_query.message.edit_text(text=txt, reply_markup=keyboard)
    await callback_query.answer(messages.SUMMONER_REMOVED)


@dp.callback_query_handler(filters.Regexp(regexp=r"cannot_.*?"))
async def cannot_do_warmup_handler(callback_query: types.CallbackQuery):
    user_id = UUID(callback_query.data.replace("cannot_", ""))
    user = await UserCRUD.get_user_by_id(user_id)
    if user.telegram_id != callback_query.from_user.id:
        return await callback_query.answer("Hey, you are not this user")

    keyboard = [
        [
            aiogram.types.inline_keyboard.InlineKeyboardButton(
                text=messages.AFTER_5_MIN, callback_data="call_after_5"
            ),
            aiogram.types.inline_keyboard.InlineKeyboardButton(
                text=messages.AFTER_10_MIN, callback_data="call_after_10"
            ),
            aiogram.types.inline_keyboard.InlineKeyboardButton(
                text=messages.AFTER_15_MIN, callback_data="call_after_15"
            ),
        ],
        [
            aiogram.types.inline_keyboard.InlineKeyboardButton(
                text=messages.NEXT_USER, callback_data="next_user"
            ),
        ]
    ]
    await callback_query.message.edit_text(
        text=callback_query.message.md_text,
        parse_mode=types.ParseMode.MARKDOWN_V2,
        entities=callback_query.message.entities,
        reply_markup=aiogram.types.inline_keyboard.InlineKeyboardMarkup(
            row_width=3, inline_keyboard=keyboard
        )
    )
    return await callback_query.answer("Got u")


@dp.callback_query_handler(filters.Regexp(regexp=r"call_after_.*?"))
async def cannot_do_warmup_handler(callback_query: types.CallbackQuery):
    minutes = int(callback_query.data.replace("call_after_", ""))
    return await callback_query.answer(f"Do it after {minutes} min")
