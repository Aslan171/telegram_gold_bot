from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def build_main_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton(text="💰Пополнить"),
        KeyboardButton(text="🌟Вывести")
    )
    kb.add(
        KeyboardButton(text="🔢Посчитать"),
        KeyboardButton(text="🆔Профиль")
    )
    kb.add(
        KeyboardButton(text="📖Помощь и ответы"),
        KeyboardButton(text="✅О боте")
    )
    kb.add(
        KeyboardButton(text="✨Продать голду"),
        KeyboardButton(text="🕹️Сменить игру")
    )

    return kb
