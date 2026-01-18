from aiogram import Bot
from db.db_utils import get_user
from aiogram.types import Message

async def notify_deposit_approved(bot: Bot, user_id: int, amount_gt: float):
    user = await get_user(user_id)
    if user:
        await bot.send_message(user_id, f"✅ Ваш баланс пополнен на сумму {amount_gt}G Голды!")

async def notify_deposit_rejected(bot: Bot, user_id: int):
    user = await get_user(user_id)
    if user:
        await bot.send_message(user_id, "❌ Пополнение отклонено")
