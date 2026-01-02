import asyncio
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties  # <- вместо ParseMode

# Проверяем, есть ли локальный .env (для разработки)
env_path = Path(".") / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path)  # загружаем только локально

# Получаем переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден! Проверьте .env (локально) или Variables (на сервере)")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не найден! Проверьте .env (локально) или Variables (на сервере)")

# Импорт хэндлеров и утилит БД
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
