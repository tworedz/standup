import re

from aiogram.types import InlineKeyboardMarkup
from crud.warmups import WarmUpSummonCRUD
from telegram import messages
from telegram.inline_keyboard.summoners import build_summoner_list_keyboard


class WarmUpSummonService:
    @classmethod
    def is_valid_summoner(cls, summoner: str) -> bool:
        usr_string = "\$me"
        mentions = re.findall(usr_string, summoner)
        return len(mentions) == 1

    @classmethod
    async def get_summoners_list_data(cls) -> tuple[str, InlineKeyboardMarkup]:
        summoners = await WarmUpSummonCRUD.get_summoners()
        keyboard = build_summoner_list_keyboard(summoners)

        if not summoners:
            txt = messages.NO_SUMMONERS
        else:
            txt = messages.SUMMONERS

        return txt, keyboard
