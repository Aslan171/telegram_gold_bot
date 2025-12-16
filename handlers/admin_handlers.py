from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import os

from db.db_utils import (
    get_pending_notifications,
    approve_deposit,
    approve_withdrawal,
    reject_deposit,
    reject_withdrawal,
    get_user
)

router = Router()
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]


# --- Команда /admin ---
@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Нет доступа.")
        return

    pending = await get_pending_notifications()
    if not pending:
        await message.answer("✅ Нет новых уведомлений.")
        return

    for p in pending:
        kb = InlineKeyboardMarkup(row_width=2)
        # кнопки для одобрения / отклонения
        if p['type'] == "deposit":
            kb.add(
                InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_deposit:{p['id']}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_deposit:{p['id']}")
            )
        elif p['type'] == "withdraw":
            kb.add(
                InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_withdraw:{p['id']}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_withdraw:{p['id']}")
            )
        text = f"ID:{p['id']} | type:{p['type']} | user:{p['user_id']} | entity:{p['entity_id']}"
        await message.answer(text, reply_markup=kb)


# --- Callback: approve deposit ---
@router.callback_query(lambda c: c.data and c.data.startswith("approve_deposit:"))
async def approve_deposit_cb(call: CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("❌ Нет доступа", show_alert=True)
        return

    try:
        deposit_id = int(call.data.split(":")[1])
    except (IndexError, ValueError):
        await call.answer("Ошибка ID", show_alert=True)
        return

    ok = await approve_deposit(deposit_id, call.from_user.id)
    await call.answer("✅ Одобрено" if ok else "❌ Уже обработано/не найдено")
    await call.message.edit_reply_markup(reply_markup=None)


# --- Callback: reject deposit ---
@router.callback_query(lambda c: c.data and c.data.startswith("reject_deposit:"))
async def reject_deposit_cb(call: CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("❌ Нет доступа", show_alert=True)
        return

    try:
        deposit_id = int(call.data.split(":")[1])
    except (IndexError, ValueError):
        await call.answer("Ошибка ID", show_alert=True)
        return

    ok = await reject_deposit(deposit_id, call.from_user.id)
    await call.answer("❌ Отклонено" if ok else "❌ Ошибка")
    await call.message.edit_reply_markup(reply_markup=None)


# --- Callback: approve withdraw ---
@router.callback_query(lambda c: c.data and c.data.startswith("approve_withdraw:"))
async def approve_withdraw_cb(call: CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("❌ Нет доступа", show_alert=True)
        return

    try:
        withdraw_id = int(call.data.split(":")[1])
    except (IndexError, ValueError):
        await call.answer("Ошибка ID", show_alert=True)
        return

    ok = await approve_withdrawal(withdraw_id, call.from_user.id)
    await call.answer("✅ Одобрено" if ok else "❌ Уже обработано/не найдено")
    await call.message.edit_reply_markup(reply_markup=None)


# --- Callback: reject withdraw ---
@router.callback_query(lambda c: c.data and c.data.startswith("reject_withdraw:"))
async def reject_withdraw_cb(call: CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("❌ Нет доступа", show_alert=True)
        return

    try:
        withdraw_id = int(call.data.split(":")[1])
    except (IndexError, ValueError):
        await call.answer("Ошибка ID", show_alert=True)
        return

    ok = await reject_withdrawal(withdraw_id, call.from_user.id)
    await call.answer("❌ Отклонено" if ok else "❌ Ошибка")
    await call.message.edit_reply_markup(reply_markup=None)
