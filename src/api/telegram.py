import asyncio
from typing import Any
from typing import Dict

from aiogram import Dispatcher
from aiogram.types import Update
from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status
from starlette.responses import Response

from core.config import settings
from sdk.dependencies import bot_dispatcher

router = APIRouter()


@router.post(
    f"/webhook/{settings.TELEGRAM_BOT_API_KEY.get_secret_value()}/",
    include_in_schema=False,
)
async def telegram_webhook(
    update_raw: Dict[str, Any], dp: Dispatcher = Depends(bot_dispatcher)
) -> Response:
    """
    Pass the new update (event from telegram) to bot dispatcher for processing.
    """
    telegram_update = Update(**update_raw)
    asyncio.create_task(dp.process_update(telegram_update))
    # await dp.process_update(telegram_update)
    return Response(status_code=status.HTTP_200_OK)
