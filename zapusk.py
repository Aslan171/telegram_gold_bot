import asyncio
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties  # <- вместо ParseMode

# Локальная разработка: подгружаем .env, если он есть
env_path = Path(".") / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path)

# Получаем переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_IDS = os.getenv("ADMIN_IDS")
CURRENCY_RATE = os.getenv("CURRENCY_RATE")
MIN_DEPOSIT = os.getenv("MIN_DEPOSIT")
WITHDRAW_MULTIPLIER = os.getenv("WITHDRAW_MULTIPLIER")

# Проверка
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден! Проверьте .env или Variables на сервере")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не найден! Проверьте .env или Variables на сервере")

# Для дебага локально или на сервере
print("BOT_TOKEN:", BOT_TOKEN)
print("DATABASE_URL:", DATABASE_URL)
print("ADMIN_IDS:", ADMIN_IDS)
