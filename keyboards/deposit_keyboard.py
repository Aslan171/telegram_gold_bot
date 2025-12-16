from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def deposit_payment_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(text="🔴Каспи"), KeyboardButton(text="⏪Перейти назад"))
    return kb

def deposit_after_receipt_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(text="Проблема с оплатой"), KeyboardButton(text="🏠Главное меню"))
    return kb
