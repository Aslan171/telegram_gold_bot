from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def withdraw_input_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(text="⬅Назад"))
    return kb

def withdraw_after_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(text="🌟Вывести"), KeyboardButton(text="💰Пополнить"))
    kb.add(KeyboardButton(text="🔢Посчитать"), KeyboardButton(text="✅О боте"))
    kb.add(KeyboardButton(text="📖Помощь и ответы"), KeyboardButton(text="✨Продать голду"))
    kb.add(KeyboardButton(text="🕹️Сменить игру"), KeyboardButton(text="🆔Профиль"))
    kb.add(KeyboardButton(text="📖Правила вывода Gold"), KeyboardButton(text="⬅Назад"))
    return kb
