from fastapi import APIRouter

from . import telegram

api_router = APIRouter()

api_router.include_router(telegram.router, prefix="/telegram", tags=["telegram"])
