from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def calc_main_kb() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton("Посчитать ₸ в G"), KeyboardButton("Посчитать G в ₸")],
        [KeyboardButton("🏠Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
