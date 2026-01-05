from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def build_main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="💰Пополнить"),
                KeyboardButton(text="🌟Вывести")
            ],
            [
                KeyboardButton(text="🔢Посчитать"),
                KeyboardButton(text="🆔Профиль")
            ],
            [
                KeyboardButton(text="✅О боте"),
                KeyboardButton(text="📖Помощь и ответы")
            ],
            [
                KeyboardButton(text="✨Продать голду"),
                KeyboardButton(text="🕹️Сменить игру")
            ],
            [
                KeyboardButton(text="📖Правила вывода Gold"),
                KeyboardButton(text="🏠Главное меню")
            ]
        ]
    )
