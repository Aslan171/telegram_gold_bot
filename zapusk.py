import asyncio
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties  # <- вместо ParseMode

# --- Локальная разработка: загружаем .env только если он есть ---
env_path = Path(".") / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path)  # подгрузка локальных переменных

# --- Получаем переменные окружения ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_IDS = os.getenv("ADMIN_IDS")
CURRENCY_RATE = os.getenv("CURRENCY_RATE")
MIN_DEPOSIT = os.getenv("MIN_DEPOSIT")
WITHDRAW_MULTIPLIER = os.getenv("WITHDRAW_MULTIPLIER")

# --- Проверка наличия обязательных переменных ---
if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN не найден! Проверьте .env (локально) или Variables (на сервере)"
    )
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL не найден! Проверьте .env (локально) или Variables (на сервере)"
    )

# --- DEBUG: покажем, что реально подхватилось ---
print("=== ENVIRONMENT CHECK ===")
print("BOT_TOKEN:", BOT_TOKEN)
print("DATABASE_URL:", DATABASE_URL)
print("ADMIN_IDS:", ADMIN_IDS)
print("=========================")

# --- Импорт хэндлеров и утилит БД ---
from handlers import menu_handlers, withdraw, deposit, calculate, admin_handlers
from db.db_utils import init_db_pool, close_db_pool

async def main():
    # Создаём бот с HTML-парсом через DefaultBotProperties
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    # FSM хранилище
    storage = MemoryStorage()

    # Диспетчер
    dp = Dispatcher(storage=storage)

    # Инициализация пула БД
    await init_db_pool(DATABASE_URL)

    # Подключаем роутеры
    dp.include_router(menu_handlers.router)
    dp.include_router(withdraw.router)
    dp.include_router(deposit.router)
    dp.include_router(calculate.router)
    dp.include_router(admin_handlers.router)

    print("Bot started")
    try:
        # Старт поллинга
        await dp.start_polling(bot)
    finally:
        # Закрываем сессию бота и пул БД
        await bot.session.close()
        await close_db_pool()

if __name__ == "__main__":
    asyncio.run(main())
