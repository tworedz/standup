import logging

from aiogram.utils.exceptions import TelegramAPIError
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


def telegram_exception_handler(request: Request, exc: TelegramAPIError):
    logger.error(f"unhandled exception: {exc.args}")
    return Response(status_code=status.HTTP_200_OK)
