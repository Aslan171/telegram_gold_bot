import os
from aiogram.types import PhotoSize

# Папка для скринов
SCREENSHOTS_DIR = "screenshots"

# Проверяем, существует ли папка, если нет — создаём
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

async def save_photo(photo: PhotoSize, user_id: int) -> str:
    """
    Сохраняет фото от пользователя и возвращает путь к файлу
    """
    # Берём наибольший размер фото
    file_id = photo.file_id
    file_path = os.path.join(SCREENSHOTS_DIR, f"{user_id}_{file_id}.jpg")
    await photo.download(destination_file=file_path)
    return file_path

