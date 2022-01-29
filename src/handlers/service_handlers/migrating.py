from core.logging import logger
from crud.users import GroupCRUD
from schemas.users import GroupMigrateSchema
from telegram.dispatcher import dp
from aiogram import types


@dp.message_handler(content_types=["migrate_to_chat_id"])
async def chat_migrating(message: types.Message) -> None:
    """Migrate chat from group to supergroup"""

    await GroupCRUD.update_group(
        message.chat.id, GroupMigrateSchema(super_group_id=message.migrate_to_chat_id)
    )
    logger.info(
        "Group migrated",
        old_group_id=message.chat.id,
        new_group_id=message.migrate_to_chat_id,
    )
