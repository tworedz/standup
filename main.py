import logging

from fastapi import FastAPI

from src.api.routers import api_router
from src.core.config import settings
from src.telegram.bot import bot

app = FastAPI()
app.include_router(api_router)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    current_url = (await bot.get_webhook_info())["url"]
    if current_url != settings.TELEGRAM_BOT_WEBHOOK_ENDPOINT:
        await bot.set_webhook(url=settings.TELEGRAM_BOT_WEBHOOK_ENDPOINT)
    logger.debug("webhook set")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Bye!")
    await bot.delete_webhook()
    await bot.close()
