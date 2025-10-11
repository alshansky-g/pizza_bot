import asyncio

import utils.logging_config as logging_config  # type: ignore
from aiogram import Bot, Dispatcher
from handlers.user_private import router as user_private_router
from utils.bot_commands import commands
from utils.config import config

bot = Bot(token=config.bot_token)

dp = Dispatcher()
dp.include_router(user_private_router)


async def main():
    await bot.set_my_commands(commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=config.allowed_updates)


if __name__ == '__main__':
    asyncio.run(main())
