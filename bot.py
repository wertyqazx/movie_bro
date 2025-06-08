import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.settings import settings
from routers import commands, search, favorites, random, genre, top250
from services.db import init_db

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_router(commands.router)
    dp.include_router(search.router)
    dp.include_router(favorites.router)
    dp.include_router(random.router)
    dp.include_router(genre.router)
    dp.include_router(top250.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
