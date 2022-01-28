import logging
import uuid

import sqlalchemy as sa
from aiogram.utils.exceptions import TelegramAPIError
from api.routers import api_router
from core.config import settings
from core.database import database
from core.scheduler import scheduler
from fastapi import FastAPI
from handlers import *  # noqa
from models import WarmUpSummon
from sdk.exceptions import telegram_exception_handler
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from telegram.bot import bot

app = FastAPI(exception_handlers={TelegramAPIError: telegram_exception_handler})

app.include_router(api_router)

logging.basicConfig(level=logging.getLevelName(settings.DEBUG_LEVEl))
logger = logging.getLogger(__name__)


@scheduler.scheduled_job("cron", day_of_week="mon-fri", hour="12,16", minute="10")
async def warmup():
    groups = await GroupCRUD.get_groups()
    summoner = await WarmUpSummonCRUD.get_random_summoner()
    user = await UserCRUD.get_random_user()
    if not summoner:
        logger.warning("There is no summoners")
        return
    if not user:
        logger.warning("There is not users")
        return

    for group in groups:
        try:
            await bot.send_message(
                chat_id=group.telegram_id,
                text=summoner.text.format(user.mention),
                parse_mode=aiogram.types.ParseMode.MARKDOWN_V2,
            )
        except aiogram.exceptions.MigrateToChat as e:
            await bot.send_message(
                chat_id=e.migrate_to_chat_id,
                text=summoner.text.format(user.mention),
                parse_mode=aiogram.types.ParseMode.MARKDOWN_V2,
            )


BASE_SUMMONERS = [
    WarmUpSummonCreateSchema(text="Just do it, {} 💪"),
    WarmUpSummonCreateSchema(text="Свистать всех наверх\! {}, веди нас 🧭"),
    WarmUpSummonCreateSchema(text="Покажи класс, {} 😎"),
    WarmUpSummonCreateSchema(text="3, 4, закончили\! {}, у тебя счастливый билет 🤞"),
    WarmUpSummonCreateSchema(text="🧛 Кошелёк или разминка, {}"),
    WarmUpSummonCreateSchema(text="Roses are red, Violets are blue, Coach is {}"),
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


@app.on_event("startup")
async def startup():
    scheduler.start()
    await database.connect()
    insert_base_summoners()

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


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    scheduler.shutdown()
    logger.info("Bye!")
    # await bot.delete_webhook()
