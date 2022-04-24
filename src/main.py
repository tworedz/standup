import asyncio
import logging
import uuid

from aiogram.utils.exceptions import TelegramAPIError
from api.routers import api_router
from core.config import settings
from core.database import database
from core.scheduler import scheduler
from fastapi import FastAPI

from crud.users import GroupCRUD
from schemas.warmups import WarmUpSummonCreateSchema
from telegram.dispatcher import dp
from handlers import *

from models import WarmUpSummon
from sdk.exceptions import telegram_exception_handler
from services.warmups import WarmUpService
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from telegram.bot import bot

app = FastAPI(exception_handlers={TelegramAPIError: telegram_exception_handler})

app.include_router(api_router)

logging.basicConfig(level=logging.getLevelName(settings.DEBUG_LEVEl))
logger = logging.getLogger(__name__)


@scheduler.scheduled_job("cron", day_of_week="mon-fri", hour="12,16")
async def warmup():
    groups = await GroupCRUD.get_groups()

    for group in groups:
        await WarmUpService.warmup(telegram_group_id=group.telegram_id)


BASE_SUMMONERS = [
    WarmUpSummonCreateSchema(text="{}, сегодня ты наш тренер 💪"),
    WarmUpSummonCreateSchema(text="Свистать всех наверх\! {}, веди нас 🧭"),
    WarmUpSummonCreateSchema(text="Покажи класс, {} 😎"),
    WarmUpSummonCreateSchema(text="🧛 Кошелёк или разминка, {}"),
    WarmUpSummonCreateSchema(text="Roses are red, Violets are blue, Coach is {}"),
    WarmUpSummonCreateSchema(text="Звёзды решили, что {} сегодня наш тренер"),
]


def insert_base_summoners() -> None:
    engine = create_engine(url=settings.DB_URI, echo=True)
    conn = engine.connect()
    for summoner in BASE_SUMMONERS:
        q = (
            insert(WarmUpSummon)
            .values(id=str(uuid.uuid4()), text=summoner.text)
            .on_conflict_do_nothing()
        )
        conn.execute(q)


async def start_bot() -> None:
    if not settings.WEBHOOK_ENABLED:
        asyncio.create_task(dp.start_polling())
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


@app.on_event("startup")
async def startup():
    scheduler.start()
    await database.connect()
    insert_base_summoners()
    await update_cron_list()
    await start_bot()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    scheduler.shutdown()
    logger.info("Bye!")
    # await bot.delete_webhook()
