import logging
import os
import sys

from aiogram.utils.exceptions import TelegramAPIError
from fastapi import FastAPI

from api.routers import api_router
from core.config import settings
from handlers import *  # noqa
from sdk.exceptions import telegram_exception_handler
from telegram.bot import bot
from aiogram import executor


app = FastAPI(exception_handlers={
    TelegramAPIError: telegram_exception_handler
})

app.include_router(api_router)

logging.basicConfig(level=logging.getLevelName(settings.DEBUG_LEVEl))
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    if not settings.WEBHOOK_ENABLED:
        await dp.start_polling()
        logger.info("Long polling started".center(79, "-"))
        return

    webhook_info = await bot.get_webhook_info()
    if not webhook_info:
        logger.error("Cannot get webhook info")
    current_url = webhook_info.url
    if current_url != settings.TELEGRAM_BOT_WEBHOOK_ENDPOINT:
        await bot.set_webhook(
            url=settings.TELEGRAM_BOT_WEBHOOK_ENDPOINT,
            drop_pending_updates=settings.TELEGRAM_DROP_PENDING_UPDATES,
        )
        logger.info(f"Webhook for url {settings.HOST_PATH} set".center(79, "-"))
    logger.info("Webhook with this url already set".center(79, "-"))


@app.on_event("shutdown")
async def shutdown():
    logger.info("Bye!")
    # await bot.delete_webhook()
