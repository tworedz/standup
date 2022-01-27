from aiogram import types
from crud.warmups import WarmUpSummonCRUD
from schemas.warmups import WarmUpSummonCreateSchema
from sdk.utils import wait_for
from services.warmups import WarmUpSummonService
from telegram import messages
from telegram.dispatcher import dp
from telegram.inline_keyboard.summoners import build_summoner_list_keyboard
from telegram.messages import NO_SUMMONERS
from telegram.messages import SUMMONERS


@dp.message_handler(commands=["summoners", "s"])
async def get_summons(message: types.Message) -> None:
    args = message.get_args()
    if not args:
        txt, keyboard = await WarmUpSummonService.get_summoners_list_data()
        response = await message.reply(text=txt, reply_markup=keyboard)
        await wait_for()
        await message.delete()
        await response.delete()
        return

    if not WarmUpSummonService.is_valid_summoner(summoner=args):
        response = await message.reply(
            messages.WRONG_SUMMONER,
            parse_mode=types.ParseMode.MARKDOWN_V2,
        )
        await wait_for()
        await response.delete()
        await message.delete()
        return

    await WarmUpSummonCRUD.create_summoner(WarmUpSummonCreateSchema(text=args))
    response = await message.reply("Summoner added!")
    await wait_for()
    await response.delete()
    await message.delete()


@dp.message_handler(commands=["schedules"])
async def get_summons(message: types.Message) -> None:
    args = message.get_args()
    if not args:
        pass
