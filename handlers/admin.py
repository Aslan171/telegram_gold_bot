from aiogram import Router, types
from utils.keyboards import admin_menu
from config import ADMIN_ID
from services.db import get_all_payments, mark_payment_done

router = Router()

# Команда /admin
@router.message(commands=["admin"])
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Доступ запрещён.")
        return

    await message.answer("👑 Админ-панель:", reply_markup=admin_menu())

# Обработка кнопок админ-панели
@router.callback_query(lambda c: c.data)
async def admin_handler(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    data = callback.data

    if data == "admin_pending":
        payments = await get_all_payments(status="pending")
        text = "⏳ Ожидание оплаты:\n"
        for p in payments:
            text += f"- {p['user_id']} | {p['amount']}₸\n"
        await callback.message.answer(text or "Нет ожидающих оплат")
        await callback.answer()
    elif data == "admin_done":
        payments = await get_all_payments(status="done")
        text = "✅ Оплаченные:\n"
        for p in payments:
            text += f"- {p['user_id']} | {p['amount']}₸\n"
        await callback.message.answer(text or "Нет оплаченных")
        await callback.answer()
    elif data.startswith("mark_done_"):
        payment_id = int(data.split("_")[-1])
        await mark_payment_done(payment_id)
        await callback.answer("✅ Отмечено как оплачено")


