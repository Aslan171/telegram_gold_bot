from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def build_main_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[  # обязательно
            [KeyboardButton(text="💰 Баланс"), KeyboardButton(text="💸 Пополнить")],
            [KeyboardButton(text="📤 Вывод"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True
    )
    return kb
