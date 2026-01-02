from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def calc_main_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(text="Посчитать ₸ в G"), KeyboardButton(text="Посчитать G в ₸"))
    kb.add(KeyboardButton(text="🏠Главное меню"))
    return kb
