from typing import Any
from typing import Dict

from aiogram import Dispatcher
from aiogram.types import Update
from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status
from starlette.responses import Response

from src.core.config import settings
from src.sdk.dependencies import bot_dispatcher
from src.sdk.dependencies import telegram_webhook_security

router = APIRouter()


@router.post(
    f"/webhook/{{secret}}/{settings.TELEGRAM_BOT_WEBHOOK_ENDPOINT}/",
    dependencies=[Depends(telegram_webhook_security)],
)
async def telegram_webhook(
    update_raw: Dict[str, Any], dp: Dispatcher = Depends(bot_dispatcher)
) -> Response:
    """
    Pass the new update (event from telegram) to bot dispatcher for processing.
    """
    telegram_update = Update(**update_raw)
    await dp.process_update(telegram_update)
    return Response(status_code=status.HTTP_200_OK)
