from aiogram import types
from aiogram.dispatcher import filters
from apscheduler.triggers.cron import CronTrigger

from core.config import settings
from crud.films import FilmCRUD
from films.exceptions import BaseFilmException
from films.exceptions import TimeoutException
from films.utils import get_movie_info
from films.utils import remove_film_job
from films.utils import update_cron_list
from schemas.films import FilmSettingUpdateOrCreateSchema
from services.chats import ChatService
from telegram.bot import bot
from telegram.dispatcher import dp


async def show_film_info(message: types.Message):
    film_setting = await FilmCRUD.get_channel_settings(telegram_channel_id=message.chat.id)
    if not film_setting or not film_setting.film_id:
        return await ChatService.reply(
            message,
            "There is no film set for this channel\nUsage: `/film https://www.cinematica.kg/movies/1440`",
            is_markdown=True,
        )
    try:
        movie_info = await get_movie_info(movie_id=film_setting.film_id)
    except BaseFilmException as e:
        return await ChatService.reply(message, str(e))

    return await ChatService.reply(message, f"Current film: `{movie_info.name}`", is_markdown=True)


async def set_film(message: types.Message, link: str):
    if not link.startswith(settings.TS_SITE):
        return await ChatService.reply(message, "Wrong link")

    _, _, str_film_id = link.rpartition("/")
    try:
        film_id = int(str_film_id)
    except ValueError:
        return await ChatService.reply(message, "Wrong film_id")

    try:
        movie_info = await get_movie_info(movie_id=film_id)
    except BaseFilmException as e:
        return await ChatService.reply(message, str(e))

    old_film = await FilmCRUD.get_channel_settings(telegram_channel_id=message.chat.id)
    if old_film:
        await remove_film_job(film=old_film)
    await FilmCRUD.update_or_create_channel_settings(
        telegram_channel_id=message.chat.id,
        data=FilmSettingUpdateOrCreateSchema(
            film_id=film_id,
        ),
    )
    await update_cron_list()
    return await ChatService.reply(
        message,
        f"Film `{movie_info.name}` successfully set",
        is_markdown=True,
    )


@dp.channel_post_handler(filters.RegexpCommandsFilter(regexp_commands=["film"]))
async def process_film_command(message: types.Message) -> None:
    """Set film"""

    link = message.get_args()
    if not link:
        return await show_film_info(message)

    return await set_film(message, link)


@dp.channel_post_handler(filters.RegexpCommandsFilter(regexp_commands=["timeout"]))
async def process_timeout_command(message: types.Message) -> None:
    """Timeout for requests"""

    raw_timeout = message.get_args()
    if not raw_timeout:
        film_settings = await FilmCRUD.get_channel_settings(telegram_channel_id=message.chat.id)
        if not film_settings:
            film_settings = await FilmCRUD.update_or_create_channel_settings(
                telegram_channel_id=message.chat.id, data=FilmSettingUpdateOrCreateSchema()
            )
        return await ChatService.reply(
            message,
            f"Current timeout: `{film_settings.timeout}`",
            is_markdown=True,
        )

    try:
        timeout = int(raw_timeout)
    except ValueError:
        return await ChatService.reply(
            message, "Wrong command\nUsage: `/timeout 30`", is_markdown=True
        )

    film_setting = await FilmCRUD.update_or_create_channel_settings(
        telegram_channel_id=message.chat.id,
        data=FilmSettingUpdateOrCreateSchema(
            timeout=timeout,
        ),
    )
    await update_cron_list()
    return await ChatService.reply(
        message,
        f"Timeout set to `{film_setting.timeout}` seconds",
        is_markdown=True,
    )


@dp.channel_post_handler(filters.RegexpCommandsFilter(regexp_commands=["cron"]))
async def process_cron_command(message: types.Message) -> None:
    """cron settings"""

    raw_cron = message.get_args()
    if not raw_cron:
        film_settings = await FilmCRUD.get_channel_settings(telegram_channel_id=message.chat.id)
        if not film_settings:
            film_settings = await FilmCRUD.update_or_create_channel_settings(
                telegram_channel_id=message.chat.id, data=FilmSettingUpdateOrCreateSchema()
            )
        return await ChatService.reply(
            message,
            f"Current cron: `{film_settings.cron}`",
            is_markdown=True,
        )

    try:
        CronTrigger.from_crontab(raw_cron)
    except ValueError:
        return await ChatService.reply(
            message, "Wrong command\nUsage: `/cron */30 * * * *`", is_markdown=True
        )

    film_setting = await FilmCRUD.update_or_create_channel_settings(
        telegram_channel_id=message.chat.id,
        data=FilmSettingUpdateOrCreateSchema(
            cron=raw_cron,
        ),
    )
    await update_cron_list()
    return await ChatService.reply(message, f"Cron set to `{film_setting.cron}`", is_markdown=True)


@dp.channel_post_handler(filters.RegexpCommandsFilter(regexp_commands=["forward_to"]))
async def process_forward_to_command(message: types.Message) -> None:
    """forward message if success"""

    raw_args = message.get_args()
    if not raw_args or raw_args.strip().split().__len__() > 1:
        return await ChatService.reply(
            message,
            "Wrong command\nUsage: `/forward_to 123456789`",
            is_markdown=True,
        )

    chat_id = raw_args.strip()
    film_setting = await FilmCRUD.update_or_create_channel_settings(
        telegram_channel_id=message.chat.id,
        data=FilmSettingUpdateOrCreateSchema(
            forward_to=chat_id
        ),
    )

    return await ChatService.reply(message, f"Forward to `{film_setting.forward_to}`", is_markdown=True)


@dp.channel_post_handler(filters.RegexpCommandsFilter(regexp_commands=["stop"]))
async def process_stop_command(message: types.Message) -> None:
    """stop"""

    await FilmCRUD.update_or_create_channel_settings(
        telegram_channel_id=message.chat.id,
        data=FilmSettingUpdateOrCreateSchema(
            is_enabled=False,
        ),
    )
    await update_cron_list()
    return await ChatService.reply(message, "Disabled")


@dp.channel_post_handler(filters.RegexpCommandsFilter(regexp_commands=["start"]))
async def process_start_command(message: types.Message) -> None:
    """start"""

    await FilmCRUD.update_or_create_channel_settings(
        telegram_channel_id=message.chat.id,
        data=FilmSettingUpdateOrCreateSchema(
            is_enabled=True,
        ),
    )
    await update_cron_list()
    return await ChatService.reply(message, "Enabled")


@dp.channel_post_handler(filters.RegexpCommandsFilter(regexp_commands=["info"]))
async def process_info_command(message: types.Message) -> None:
    """info"""

    film_setting = await FilmCRUD.get_channel_settings(telegram_channel_id=message.chat.id)
    return await ChatService.reply(message, film_setting.__repr__())
