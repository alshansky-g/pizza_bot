import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import utils.logging_config as logging_config  # type: ignore
from database.engine import create_db, session_maker
from handlers.admin_private import router as admin_router
from handlers.user_group import router as user_group_router
from handlers.user_private import router as user_private_router
from middlewares.db import DataBaseSession
from utils.config import config

bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.update.middleware(DataBaseSession(session_maker))
dp.include_router(admin_router)
dp.include_router(user_private_router)
dp.include_router(user_group_router)


async def main():
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), admins_list=config.admins_list)


if __name__ == "__main__":
    asyncio.run(main())
