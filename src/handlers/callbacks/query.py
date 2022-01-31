from datetime import datetime
from datetime import timedelta
from uuid import UUID

import aiogram.types.inline_keyboard
from aiogram import types
from aiogram import filters
from core.logging import logger
from crud.users import UserCRUD
from crud.warmups import WarmUpSummonCRUD
from sdk.utils import wait_for
from services.warmups import WarmUpSummonService
from telegram import messages
from telegram.dispatcher import dp
from telegram.inline_keyboard.summoners import build_warmup_keyboard


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
                text=messages.AFTER_5_MIN, callback_data=f"call_after:5:{user_id}"
            ),
            aiogram.types.inline_keyboard.InlineKeyboardButton(
                text=messages.AFTER_10_MIN, callback_data=f"call_after:10:{user_id}"
            ),
            aiogram.types.inline_keyboard.InlineKeyboardButton(
                text=messages.AFTER_15_MIN, callback_data=f"call_after:15:{user_id}"
            ),
        ],
        [
            aiogram.types.inline_keyboard.InlineKeyboardButton(
                text=messages.NEXT_USER, callback_data="next_user"
            ),
        ],
    ]
    await callback_query.message.edit_text(
        text=callback_query.message.md_text,
        parse_mode=types.ParseMode.MARKDOWN_V2,
        reply_markup=aiogram.types.inline_keyboard.InlineKeyboardMarkup(
            row_width=3, inline_keyboard=keyboard
        ),
    )
    return await callback_query.answer("Got u")


@dp.callback_query_handler(filters.Regexp(regexp=r"call_after:\d+:.*?"))
async def cannot_do_warmup_handler(callback_query: types.CallbackQuery):
    _, minutes, user_id = callback_query.data.split(":")
    minutes = int(minutes)
    user_id = UUID(user_id)
    user = await UserCRUD.get_user_by_id(user_id)
    if user.telegram_id != callback_query.from_user.id:
        return await callback_query.answer("Hey, you are not this user")

    await callback_query.answer(f"OK, I do it after {minutes} min", show_alert=True)
    next_warmup = datetime.now() + timedelta(minutes=minutes)
    next_warmup_time = next_warmup.strftime("%H:%M")
    text = f"{callback_query.message.md_text}\n\nWarmup moved to {next_warmup_time}"
    await callback_query.message.edit_text(
        text=text,
        parse_mode=types.ParseMode.MARKDOWN_V2,
        reply_markup=None,
    )
    await wait_for(minutes * 60)
    await callback_query.message.reply(
        text=callback_query.from_user.get_mention(),
        parse_mode=types.ParseMode.MARKDOWN_V2,
    )
    return True


@dp.callback_query_handler(filters.Regexp(regexp=r"next_user"))
async def cannot_do_warmup_handler(callback_query: types.CallbackQuery):
    admins = await callback_query.message.chat.get_administrators()
    admin_ids = [admin.user.id for admin in admins]
    if callback_query.message.from_user.id not in admin_ids:
        return await callback_query.answer("Hey, you are not admin", show_alert=True)

    await callback_query.message.edit_text(
        text=callback_query.message.md_text,
        parse_mode=types.ParseMode.MARKDOWN_V2,
        reply_markup=None,
    )

    user = await WarmUpSummonService.get_warmup_user(
        group_telegram_id=callback_query.message.chat.id
    )
    summoner = await WarmUpSummonCRUD.get_random_summoner()
    keyboard = build_warmup_keyboard(user)

    await callback_query.message.reply(
        text=summoner.text.format(user.mention),
        parse_mode=types.ParseMode.MARKDOWN_V2,
        reply_markup=keyboard,
    )
    return True
