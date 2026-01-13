from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def build_main_kb() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton("💰Пополнить"), KeyboardButton("🌟Вывести")],
        [KeyboardButton("🔢Посчитать"), KeyboardButton("🆔Профиль")],
        [KeyboardButton("✅О боте"), KeyboardButton("📖Помощь и ответы")],
        [KeyboardButton("✨Продать голду"), KeyboardButton("🕹️Сменить игру")],
    ]
    kb = ReplyKeyboardMarkup()
    kb.keyboard = keyboard
    kb.resize_keyboard = True
    return kb
