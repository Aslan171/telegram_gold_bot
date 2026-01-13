from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- Ввод суммы для вывода ---
def withdraw_input_kb() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton("⬅ Назад")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Меню после вывода ---
def withdraw_after_kb() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton("🌟Вывести"), KeyboardButton("💰Пополнить")],
        [KeyboardButton("🔢Посчитать"), KeyboardButton("✅О боте")],
        [KeyboardButton("📖Помощь и ответы"), KeyboardButton("✨Продать голду")],
        [KeyboardButton("🕹️Сменить игру"), KeyboardButton("🆔Профиль")],
        [KeyboardButton("📖Правила вывода Gold"), KeyboardButton("⬅ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
