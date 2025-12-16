import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from dotenv import load_dotenv
import os

# load env
load_dotenv()

from handlers import menu_handlers, withdraw, deposit, calculate, admin_handlers
from db.db_utils import init_db_pool, close_db_pool

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    # Используем DefaultBotProperties вместо parse_mode напрямую
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # init db pool
    await init_db_pool(os.getenv("DATABASE_URL"))

    # include handlers (each module exposes `router`)
    dp.include_router(menu_handlers.router)
    dp.include_router(withdraw.router)
    dp.include_router(deposit.router)
    dp.include_router(calculate.router)
    dp.include_router(admin_handlers.router)

    print("Bot started")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await close_db_pool()

if __name__ == "__main__":
    asyncio.run(main())
