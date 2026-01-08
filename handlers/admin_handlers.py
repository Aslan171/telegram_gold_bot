from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import os

from db.db_utils import (
    get_pending_notifications,
    approve_deposit,
    reject_deposit,
    approve_withdrawal,
    reject_withdrawal,
)
from keyboards.admin_keyboard import get_admin_kb, notification_kb

router = Router()
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# -----------------------------
# /admin command
# -----------------------------
@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Нет доступа.")
        return

    kb = await get_admin_kb()
    await message.answer("👑 Панель администратора", reply_markup=kb)


# -----------------------------
# Просмотр всех уведомлений
# -----------------------------
@router.callback_query(F.data == "admin_view_notifications")
async def view_notifications_cb(call: CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("❌ Нет доступа", show_alert=True)
        return

    pending = await get_pending_notifications()
    if not pending:
        await call.answer("✅ Новых уведомлений нет", show_alert=True)
        return

    for p in pending:
        kb = notification_kb(p['id'], p['type'])
        text = (
            f"📌 Notification ID: {p['id']}\n"
            f"Type: {p['type']}\n"
            f"User ID: {p['user_id']}\n"
            f"Entity ID: {p['entity_id']}"
        )
        await call.message.answer(text, reply_markup=kb)
    await call.answer()


# -----------------------------
# Универсальный callback для админа
# -----------------------------
async def handle_admin_cb(call: CallbackQuery, action: str, entity: str):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("❌ Нет доступа", show_alert=True)
        return

    try:
        entity_id = int(call.data.split(":")[1])
    except (IndexError, ValueError):
        await call.answer("❌ Ошибка ID", show_alert=True)
        return

    func_map = {
        "approve_deposit": approve_deposit,
        "reject_deposit": reject_deposit,
        "approve_withdraw": approve_withdrawal,
        "reject_withdraw": reject_withdrawal
    }

    key = f"{action}_{entity}"
    if key not in func_map:
        await call.answer("❌ Неизвестная операция", show_alert=True)
        return

    ok = await func_map[key](entity_id, call.from_user.id)
    text_ok = "✅ Одобрено" if action == "approve" and ok else "❌ Отклонено / ошибка"
    await call.answer(text_ok)
    await call.message.edit_reply_markup(reply_markup=None)


# -----------------------------
# Регистрация callback
# -----------------------------
@router.callback_query(lambda c: c.data and c.data.startswith(
    ("approve_deposit:", "reject_deposit:", "approve_withdraw:", "reject_withdraw:")
))
async def admin_callback(call: CallbackQuery):
    parts = call.data.split("_")
    action = parts[0]       # approve / reject
    entity = parts[1].split(":")[0]  # deposit / withdraw
    await handle_admin_cb(call, action, entity)
