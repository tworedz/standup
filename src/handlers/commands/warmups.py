from aiogram import types

from crud.users import UserCRUD
from crud.warmups import WarmUpSummonCRUD
from schemas.warmups import WarmUpSummonCreateSchema
from sdk.utils import wait_for
from services.chats import ChatService
from services.warmups import WarmUpSummonService
from telegram import messages
from telegram.dispatcher import dp
from telegram.inline_keyboard.summoners import build_warmup_keyboard


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

    try:
        summoner = WarmUpSummonCreateSchema(text=args)
    except ValueError:
        response = await message.reply(
            messages.WRONG_SUMMONER,
            parse_mode=types.ParseMode.MARKDOWN_V2,
        )
        await wait_for()
        await response.delete()
        await message.delete()
        return

    await WarmUpSummonCRUD.create_summoner(summoner)
    response = await message.reply("Summoner added!")
    await wait_for()
    await response.delete()
    await message.delete()


@dp.message_handler(commands=["w"])
async def warmup(message: types.Message) -> None:
    users = await UserCRUD.get_group_users(telegram_id=message.chat.id)
    if not users:
        await ChatService.reply(message, "No one joined to this group(")
        return

    user = await WarmUpSummonService.get_warmup_user(group_telegram_id=message.chat.id)
    summoner = await WarmUpSummonCRUD.get_random_summoner()
    keyboard = build_warmup_keyboard(user)

    await ChatService.reply(
        message, text=summoner.text.format(user.mention), reply_markup=keyboard, is_markdown=True
    )
