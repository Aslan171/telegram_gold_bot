from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- Ввод суммы для вывода ---
def withdraw_input_kb() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton("⬅ Назад")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Меню после вывода ---
def withdraw_after_kb() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="🌟Вывести"), KeyboardButton(text="💰Пополнить")],
        [KeyboardButton(text="🔢Посчитать"), KeyboardButton(text="✅О боте")],
        [KeyboardButton(text="📖Помощь и ответы"), KeyboardButton(text="✨Продать голду")],
        [KeyboardButton(text="🕹️Сменить игру"), KeyboardButton(text="🆔Профиль")],
        [KeyboardButton(text="📖Правила вывода Gold"), KeyboardButton(text="⬅ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
