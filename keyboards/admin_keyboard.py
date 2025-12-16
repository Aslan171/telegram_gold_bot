from aiogram import Router, F
from aiogram.types import Message
from keyboards.admin_keyboard import get_admin_kb
from dotenv import load_dotenv
import os

load_dotenv()
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

router = Router()

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет доступа к этой команде.")
        return

    kb = await get_admin_kb()  # если get_admin_kb асинхронная
    await message.answer("👑 Панель администратора", reply_markup=kb)
