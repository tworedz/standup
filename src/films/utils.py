from typing import Any

import apscheduler.jobstores
import httpx
from aiogram import types
from apscheduler.triggers.cron import CronTrigger

from core.logging import logger
from core.scheduler import scheduler
from crud.films import FilmCRUD
from films.exceptions import BaseFilmException
from films.exceptions import NotFoundException
from films.exceptions import TimeoutException
from films.exceptions import UnexpectedException
from schemas.films import BookResponse
from schemas.films import Cinema
from schemas.films import FilmSchema
from schemas.films import FilmSettingSchema
from telegram.bot import bot


async def _get(url: str, timeout: int) -> Any:
    client = httpx.AsyncClient()
    try:
        result = await client.get(url, timeout=timeout)
        result.raise_for_status()
    except httpx.ConnectTimeout:
        raise TimeoutException(url=url, timeout=timeout)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == httpx.codes.NOT_FOUND:
            raise NotFoundException(url=url)
        logger.error(f"Unexpected for {url}", error=str(e), status_code=e.response.status_code)
        raise UnexpectedException(error=str(e), status_code=e.response.status_code)
    finally:
        await client.aclose()

    return result


async def get_movie_info(movie_id: int, timeout: int = 5) -> FilmSchema:
    url = f"https://cinematica.kg/api/v1/movies/{movie_id}"
    result = await _get(url=url, timeout=timeout)
    return FilmSchema.parse_obj(result.json())


def get_movie_page_url(movie_id: int) -> str:
    return f"https://www.cinematica.kg/movies/{movie_id}"


async def get_film_cinemas(film_id: int, timeout: int) -> dict[str, Cinema]:
    url = f"https://cinematica.kg/api/v1/repertory/movie/{film_id}/grouped"
    result = await _get(url=url, timeout=timeout)

    response = BookResponse.parse_obj(result.json())
    books = response.list
    _cinemas = {book.cinema for book in books}
    _cinemas = [Cinema(cinema=cinema) for cinema in _cinemas]
    cinemas: dict[str, Cinema] = {cinema.cinema: cinema for cinema in _cinemas}
    for book in books:
        cinemas[book.cinema].dates.append(f"{book.date} в {book.time}")
    return cinemas


async def check_film(telegram_channel_id: int, film_id: int, timeout: int = 5):
    try:
        movie_info = await get_movie_info(film_id)
    except BaseFilmException as e:
        return await bot.send_message(chat_id=telegram_channel_id, text=str(e))

    try:
        cinemas = await get_film_cinemas(film_id, timeout)
    except BaseFilmException as e:
        return await bot.send_message(chat_id=telegram_channel_id, text=str(e))

    is_exist = bool(cinemas)
    mark = "✅" if is_exist else "❌"
    text = f"""{mark}<a href="{get_movie_page_url(film_id)}"><b>{movie_info.name}</b></a>\n\n"""
    if is_exist:
        for cinema in cinemas.values():
            text += f"<b>{cinema.cinema}</b>:\n"
            for date in cinema.dates:
                text += f"\t{date}\n"
    else:
        text += "<i>Пока нет броней</i>"

    await bot.send_message(
        telegram_channel_id,
        text=text,
        parse_mode=types.ParseMode.HTML,
        disable_notification=not is_exist
    )


def get_film_job_id(film: FilmSettingSchema) -> str:
    return f"film_job_{film.telegram_channel_id}_{film.film_id}"


async def remove_film_job(film: FilmSettingSchema) -> None:
    try:
        scheduler.remove_job(get_film_job_id(film))
    except apscheduler.jobstores.base.JobLookupError:
        pass


async def update_cron_list() -> None:
    films = await FilmCRUD.get_channels()
    for film in films:
        try:
            scheduler.remove_job(get_film_job_id(film))
        except apscheduler.jobstores.base.JobLookupError:
            pass
        scheduler.add_job(
            func=check_film,
            trigger=CronTrigger.from_crontab(film.cron),
            kwargs={
                "telegram_channel_id": film.telegram_channel_id,
                "film_id": film.film_id,
                "timeout": film.timeout,
            },
            id=get_film_job_id(film),
        )
