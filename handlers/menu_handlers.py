import asyncio
import os
from pathlib import Path
from decimal import Decimal

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

# --- Load .env if exists ---
env_path = Path(".") / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path)

# --- ENV vars ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
CURRENCY_RATE = Decimal(os.getenv("CURRENCY_RATE", "5.5"))
MIN_DEPOSIT = Decimal(os.getenv("MIN_DEPOSIT", "100"))
WITHDRAW_MULTIPLIER = Decimal(os.getenv("WITHDRAW_MULTIPLIER", "1.0"))

# --- Mandatory check ---
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден!")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не найден!")

# --- Debug info ---
print("=== ENV CHECK ===")
print("BOT_TOKEN:", BOT_TOKEN)
print("DATABASE_URL:", DATABASE_URL)
print("ADMIN_IDS:", ADMIN_IDS)
print("CURRENCY_RATE:", CURRENCY_RATE)
print("MIN_DEPOSIT:", MIN_DEPOSIT)
print("WITHDRAW_MULTIPLIER:", WITHDRAW_MULTIPLIER)
print("=================")

# --- Imports ---
from handlers import menu_handlers, withdraw, deposit, calculate, admin_handlers
from db.db_utils import init_db_pool, close_db_pool

async def main():
    # --- Bot & Dispatcher ---
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # --- Init DB ---
    await init_db_pool()

    # --- Register routers ---
    dp.include_router(menu_handlers.router)
    dp.include_router(withdraw.router)
    dp.include_router(deposit.router)
    dp.include_router(calculate.router)
    dp.include_router(admin_handlers.router)

    print("Bot started")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print("❌ Bot crashed:", e)
    finally:
        await bot.session.close()
        await close_db_pool()

if __name__ == "__main__":
    asyncio.run(main())

