import random
import re

from aiogram.types import InlineKeyboardMarkup

from crud.users import UserCRUD
from crud.warmups import WarmupQueueCRUD
from crud.warmups import WarmUpSummonCRUD
from models import WarmupQueue
from schemas.users import UserSchema
from schemas.warmups import WarmupQueueCreateSchema
from schemas.warmups import WarmupQueueUpdateSchema
from telegram import messages
from telegram.inline_keyboard.summoners import build_summoner_list_keyboard


class WarmUpSummonService:
    @classmethod
    async def get_summoners_list_data(cls) -> tuple[str, InlineKeyboardMarkup]:
        summoners = await WarmUpSummonCRUD.get_summoners()
        keyboard = build_summoner_list_keyboard(summoners)

        if not summoners:
            txt = messages.NO_SUMMONERS
        else:
            txt = messages.SUMMONERS

        return txt, keyboard

    @classmethod
    async def get_warmup_user(cls, group_telegram_id: int) -> UserSchema:
        queue = await WarmupQueueCRUD.get_queue(group_telegram_id)
        if not queue or not queue.user_ids:
            users = await UserCRUD.get_group_users(telegram_id=group_telegram_id)
            randomized = cls.shuffle_users(users)
            user_ids = [user.id for user in randomized]
            if not queue:
                queue = await WarmupQueueCRUD.create_queue(
                    group_telegram_id, data=WarmupQueueCreateSchema(user_ids=user_ids)
                )
            else:
                queue = await WarmupQueueCRUD.update_queue(
                    group_telegram_id, data=WarmupQueueUpdateSchema(user_ids=user_ids)
                )

        user_id, *others = queue.user_ids
        await WarmupQueueCRUD.update_queue(
            group_telegram_id, WarmupQueueUpdateSchema(user_ids=others)
        )
        return await UserCRUD.get_user_by_id(user_id=user_id)

    @classmethod
    def shuffle_users(cls, items: list[UserSchema]) -> list[UserSchema]:
        return random.sample(items, len(items))
