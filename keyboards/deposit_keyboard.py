from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- Выбор метода оплаты ---
def deposit_method_kb() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="🔴 Каспи", callback_data="deposit_method:kaspi"),
         InlineKeyboardButton(text="⏪ Перейти назад", callback_data="deposit_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

# --- После отправки квитанции ---
def deposit_after_receipt_kb() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="Проблема с оплатой", callback_data="deposit_problem"),
         InlineKeyboardButton(text="🏠 Главное меню", callback_data="deposit_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

# --- Подтверждение оплаты (после выбора метода) ---
def deposit_confirm_kb(amount: float, card_number: str) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data="deposit_paid"),
         InlineKeyboardButton(text="❌ Отмена", callback_data="deposit_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
