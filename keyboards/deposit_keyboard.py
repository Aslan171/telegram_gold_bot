from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- Выбор метода оплаты ---
def deposit_method_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.inline_keyboard = [
        [InlineKeyboardButton("🔴 Каспи", callback_data="deposit_method:kaspi"),
         InlineKeyboardButton("⏪ Перейти назад", callback_data="deposit_cancel")]
    ]
    return kb

# --- После отправки квитанции ---
def deposit_after_receipt_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.inline_keyboard = [
        [InlineKeyboardButton("Проблема с оплатой", callback_data="deposit_problem"),
         InlineKeyboardButton("🏠 Главное меню", callback_data="deposit_cancel")]
    ]
    return kb

# --- Подтверждение оплаты (после выбора метода) ---
def deposit_confirm_kb(amount: float, card_number: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.inline_keyboard = [
        [InlineKeyboardButton("✅ Я оплатил", callback_data="deposit_paid"),
         InlineKeyboardButton("❌ Отмена", callback_data="deposit_cancel")]
    ]
    return kb
