import asyncio

from aiogram import types

from crud.warmups import WarmUpSummonCRUD
from schemas.warmups import WarmUpSummonCreateSchema
from services.warmups import WarmUpSummonService
from telegram.dispatcher import dp


@dp.message_handler(commands=["summoners", "s"])
async def get_summons(message: types.Message) -> None:
    args = message.get_args()
    if not args:
        summoners = await WarmUpSummonCRUD.get_summoners()
        txt = "\n".join([summoner.summoner for summoner in summoners])
        if not txt:
            txt = "There is no drama"
        response = await message.reply(txt)
        await asyncio.sleep(5)
        await message.delete()
        await response.delete()
        return

    if not WarmUpSummonService.is_valid_summoner(summoner=args):
        response = await message.reply(
            "Wrong summoner\!\nUsage: `/s Go, $me, Go\!`", parse_mode=types.ParseMode.MARKDOWN_V2,
        )
        await asyncio.sleep(5)
        await response.delete()
        await message.delete()
        return

    await WarmUpSummonCRUD.create_summoner(WarmUpSummonCreateSchema(summoner=args))
    response = await message.reply("Summoner added!")
    await asyncio.sleep(5)
    await response.delete()
    await message.delete()
