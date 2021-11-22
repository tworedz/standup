import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.utils import executor
from fastapi import FastAPI


app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
HOST_PATH = os.environ.get("HOST_PATH")
WEBHOOK_PATH = ""
WEBHOOK_URL = f"{HOST_PATH}/{WEBHOOK_PATH}"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "custom"])
async def echo(message: types.Message):
    await message.answer(f"{message.text} {message.values} {message.chat.id}")
    logger.info(f"message was: {message.text}")


async def on_webhook_start():
    await bot.set_webhook(WEBHOOK_URL)
    logger.debug("webhook set")


async def on_webhook_shutdown():
    await bot.delete_webhook()
    logger.debug("webhook removed")


@app.on_event("startup")
async def startup():
    logger.info("Bot session started...")
    await executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_URL,
        on_startup=on_webhook_start,
        on_shutdown=on_webhook_shutdown,
        skip_updates=True,
    )


@app.on_event("shutdown")
async def shutdown():
    logger.info("Bye!")
    await bot.close()


@app.get("/{name:str}/{age:int}")
async def main(name: str, age: int):
    await bot.send_message(chat_id="356038961", text=f"{name}")
    return {
        "name": name,
        "age": age,
    }


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
