from dataclasses import dataclass
from dotenv import load_dotenv
import os

@dataclass
class Config:
    bot_token: str
    admin_ids: list[int]
    rate_tenge_per_g: int  # <-- добавили

def load_config() -> Config:
    load_dotenv()  # загружает .env

    bot_token = os.getenv("BOT_TOKEN")
    admin_raw = os.getenv("ADMIN_IDS", "")

    # Преобразование строки "123,456" → [123, 456]
    admin_ids = []
    if admin_raw:
        admin_ids = [int(x) for x in admin_raw.split(",") if x.strip().isdigit()]

    if not bot_token:
        raise ValueError("BOT_TOKEN не найден. Укажи его в .env.")

    rate_tenge_per_g = int(os.getenv("RATE_TENGE_PER_G", 5000))  # значение по умолчанию 5000

    return Config(
        bot_token=bot_token,
        admin_ids=admin_ids,
        rate_tenge_per_g=rate_tenge_per_g
    )



