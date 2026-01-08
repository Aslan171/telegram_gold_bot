from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔔 Уведомления", callback_data="admin_view_notifications"),
        InlineKeyboardButton("⚙ Настройки", callback_data="admin_settings")
    )
    return kb

def notification_kb(notification_id: int, notif_type: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    if notif_type == "deposit":
        kb.add(
            InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_deposit:{notification_id}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_deposit:{notification_id}")
        )
    elif notif_type == "withdraw":
        kb.add(
            InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_withdraw:{notification_id}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_withdraw:{notification_id}")
        )
    return kb
