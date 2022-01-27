from aiogram.types import inline_keyboard
from schemas.warmups import WarmUpSummonSchema


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
