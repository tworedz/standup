import random
from typing import Optional
from uuid import UUID

from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from crud.users import UserCRUD
from crud.warmups import WarmUpCRUD
from crud.warmups import WarmupQueueCRUD
from crud.warmups import WarmUpSummonCRUD
from schemas.users import UserSchema
from schemas.warmups import WarmUpCreateSchema
from schemas.warmups import WarmupQueueCreateSchema
from schemas.warmups import WarmupQueueUpdateSchema
from schemas.warmups import WarmUpSchema
from schemas.warmups import WarmUpUpdateSchema
from telegram import messages
from telegram.bot import bot
from telegram.inline_keyboard.summoners import build_summoner_list_keyboard
from telegram.inline_keyboard.summoners import build_warmup_keyboard


class WarmUpService:
    @classmethod
    async def warmup(cls, telegram_group_id: int) -> None:
        user = await WarmUpSummonService.get_warmup_user(group_telegram_id=telegram_group_id)
        summoner = await WarmUpSummonCRUD.get_random_summoner()
        keyboard = build_warmup_keyboard(user)
        await WarmUpCRUD.create_warmup(
            data=WarmUpCreateSchema(
                user_id=user.id, telegram_group_id=telegram_group_id, warmup_summon_id=summoner.id
            )
        )

        await bot.send_message(
            chat_id=telegram_group_id,
            text=summoner.text.format(user.mention),
            parse_mode=types.ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )

    @classmethod
    async def get_warmup(cls, user_id: UUID, telegram_group_id: int) -> Optional[WarmUpSchema]:
        return await WarmUpCRUD.get_warmup(user_id=user_id, telegram_group_id=telegram_group_id)

    @classmethod
    async def update_warmup(
        cls, user_id: UUID, telegram_group_id: int, data: WarmUpUpdateSchema
    ) -> WarmUpSchema:
        return await WarmUpCRUD.update_warmup(
            user_id=user_id, telegram_group_id=telegram_group_id, data=data
        )


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
