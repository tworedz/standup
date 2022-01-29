from aiogram.types import inline_keyboard

from schemas.users import UserSchema
from schemas.warmups import WarmUpSummonSchema
from telegram import messages


def build_summoner_list_keyboard(
    summoners: list[WarmUpSummonSchema],
) -> inline_keyboard.InlineKeyboardMarkup:
    keyboard = []
    for summoner in summoners:
        row = [
            inline_keyboard.InlineKeyboardButton(text=summoner.text, callback_data="/dev/null"),
            inline_keyboard.InlineKeyboardButton(
                text="➖", callback_data=f"remove_summoner_{summoner.id}"
            ),
        ]
        keyboard.append(row)

    return inline_keyboard.InlineKeyboardMarkup(row_width=2, inline_keyboard=keyboard)


def build_warmup_keyboard(user: UserSchema) -> inline_keyboard.InlineKeyboardMarkup:
    keyboard = []
    cannot_btn = [
        inline_keyboard.InlineKeyboardButton(
            text=messages.CANNOT_DO_WARMUP, callback_data=f"cannot_{user.id}"
        ),
        inline_keyboard.InlineKeyboardButton(
            text=messages.NEXT_USER, callback_data="next_user"
        )
    ]
    keyboard.append(cannot_btn)
    return inline_keyboard.InlineKeyboardMarkup(row_width=1, inline_keyboard=keyboard)
