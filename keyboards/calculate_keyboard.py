from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def calc_main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup()
    kb.keyboard = [
        [KeyboardButton("Посчитать ₸ в G"), KeyboardButton("Посчитать G в ₸")],
        [KeyboardButton("🏠Главное меню")]
    ]
    kb.resize_keyboard = True
    return kb
