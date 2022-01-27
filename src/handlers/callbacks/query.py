from uuid import UUID

import aiogram.types
from core.logging import logger
from crud.warmups import WarmUpSummonCRUD
from services.warmups import WarmUpSummonService
from telegram import messages
from telegram.dispatcher import dp


@dp.callback_query_handler(aiogram.filters.Regexp(regexp=r"remove_summoner_.*?"))
async def remove_summoner_handler(callback_query: aiogram.types.CallbackQuery) -> None:
    summoner_id = UUID(callback_query.data.replace("remove_summoner_", ""))
    try:
        await WarmUpSummonCRUD.delete_summoner(summoner_id)
    except Exception as e:
        logger.warning("Summoner not found", error=e)
        return

    txt, keyboard = await WarmUpSummonService.get_summoners_list_data()
    await callback_query.message.edit_text(text=txt, reply_markup=keyboard)
    await callback_query.answer(messages.SUMMONER_REMOVED)
