from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def withdraw_input_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("⬅Назад"))
    return kb

def withdraw_after_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🌟Вывести"), KeyboardButton("💰Пополнить"))
    kb.add(KeyboardButton("🔢Посчитать"), KeyboardButton("✅О боте"))
    kb.add(KeyboardButton("📖Помощь и ответы"), KeyboardButton("✨Продать голду"))
    kb.add(KeyboardButton("🕹️Сменить игру"), KeyboardButton("🆔Профиль"))
    kb.add(KeyboardButton("📖Правила вывода Gold"), KeyboardButton("⬅Назад"))
    return kb
