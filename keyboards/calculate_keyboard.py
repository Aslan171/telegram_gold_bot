from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def calc_main_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("Посчитать ₸ в G"),
        KeyboardButton("Посчитать G в ₸")
    )
    kb.add(KeyboardButton("🏠Главное меню"))
    return kb
