from typing import Dict

import httpx
from aiogram import types

from core.config import settings
from main import logger, app
from schemas.films import FilmSchema, BookResponse, Cinema
from telegram.bot import bot


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
