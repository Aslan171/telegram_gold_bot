from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_admin_kb() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="🔔 Уведомления", callback_data="admin_view_notifications"),
         InlineKeyboardButton(text="⚙ Настройки", callback_data="admin_settings")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def notification_kb(notification_id: int, notif_type: str) -> InlineKeyboardMarkup:
    if notif_type == "deposit":
        inline_keyboard = [
            [InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_deposit:{notification_id}"),
             InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_deposit:{notification_id}")]
        ]
    elif notif_type == "withdraw":
        inline_keyboard = [
            [InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_withdraw:{notification_id}"),
             InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_withdraw:{notification_id}")]
        ]
    else:
        inline_keyboard = [
            [InlineKeyboardButton(text="❌ Неизвестный тип", callback_data="none")]
        ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
