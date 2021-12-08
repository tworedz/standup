import logging
from typing import Dict
from typing import List

import aiogram
import httpx
import os
import sys

import fastapi_utils
from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from pydantic import parse_obj_as

from api.routers import api_router
from core.config import settings
from handlers import *  # noqa
from schemas.films import BookResponse
from schemas.films import Cinema
from schemas.films import FilmSchema
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


async def get_movie_info(movie_id: int) -> FilmSchema:
    url = f"https://cinematica.kg/api/v1/movies/{movie_id}"
    client = httpx.AsyncClient()
    try:
        result = await client.get(url, timeout=settings.TIMEOUT)
    except httpx._exceptions.ConnectTimeout:
        logger.error(f"Timeout for {url}")
        return
    finally:
        await client.aclose()
    return FilmSchema.parse_obj(result.json())


def get_movie_page_url(movie_id: int) -> str:
    return f"https://www.cinematica.kg/movies/{movie_id}"


@app.on_event("startup")
@repeat_every(seconds=settings.REPEAT_EVERY)
async def check_film():
    url = f"https://cinematica.kg/api/v1/repertory/movie/{settings.FILM_ID}/grouped"
    client = httpx.AsyncClient()
    try:
        result = await client.get(url, timeout=settings.TIMEOUT)
    except httpx._exceptions.ConnectTimeout:
        logger.error(f"Timeout for {url}")
        return
    finally:
        await client.aclose()

    if result is None:
        logger.error("Cannot get url")
        return

    if result.status_code != httpx._status_codes.codes.OK:
        logger.warning("Something went wrong", status=result.status_code)
        return

    movie_info = await get_movie_info(settings.FILM_ID)
    movie_name = movie_info.name if movie_info else "NOT FOUND"

    response = BookResponse.parse_obj(result.json())
    books = response.list
    _cinemas = {book.cinema for book in books}
    _cinemas = [Cinema(cinema=cinema) for cinema in _cinemas]
    cinemas: Dict[str, Cinema] = {cinema.cinema: cinema for cinema in _cinemas}
    for book in books:
        cinemas[book.cinema].dates.append(f"{book.date} в {book.time}")
    text = f"""<a href="{get_movie_page_url(settings.FILM_ID)}"><b>{movie_name}</b></a>\n"""
    for cinema in cinemas.values():
        text += f"<b>{cinema.cinema}</b>:\n"
        for date in cinema.dates:
            text += f"\t{date}\n"
    else:
        text += "Пока нет броней"

    await bot.send_message(settings.CHANNEL_ID, text=text, parse_mode=types.ParseMode.HTML)


@app.on_event("shutdown")
async def shutdown():
    logger.info("Bye!")
    # await bot.delete_webhook()
