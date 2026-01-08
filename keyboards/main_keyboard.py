from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def build_main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("💰Пополнить"))
    kb.add(KeyboardButton("🌟Вывести"))
    kb.add(KeyboardButton("🔢Посчитать"))
    kb.add(KeyboardButton("🆔Профиль"))
    kb.add(KeyboardButton("✅О боте"))
    kb.add(KeyboardButton("📖Помощь и ответы"))
    kb.add(KeyboardButton("✨Продать голду"))
    kb.add(KeyboardButton("🕹️Сменить игру"))
    return kb
