from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def build_main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # 2 кнопки в ряд

    # Добавляем кнопки построчно
    kb.add(
        KeyboardButton("💰Пополнить"),
        KeyboardButton("🌟Вывести")
    )
    kb.add(
        KeyboardButton("🔢Посчитать"),
        KeyboardButton("🆔Профиль")
    )
    kb.add(
        KeyboardButton("✅О боте"),
        KeyboardButton("📖Помощь и ответы")
    )
    kb.add(
        KeyboardButton("✨Продать голду"),
        KeyboardButton("🕹️Сменить игру")
    )

    return kb
