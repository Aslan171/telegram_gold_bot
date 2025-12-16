from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Конфиг для подключения к PostgreSQL
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),  # по умолчанию 5432
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# ID администратора (можно добавить, если нужно)
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))  # вставишь свой Telegram ID

