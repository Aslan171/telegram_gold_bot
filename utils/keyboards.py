from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===================== Главное меню =====================
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Вывести", callback_data="menu_withdraw"),
        InlineKeyboardButton("Пополнить", callback_data="menu_deposit"),
        InlineKeyboardButton("Посчитать", callback_data="menu_calc"),
        InlineKeyboardButton("О боте", callback_data="menu_about"),
        InlineKeyboardButton("Помощь и ответы", callback_data="menu_help"),
        InlineKeyboardButton("Продать голду", callback_data="menu_sell"),
        InlineKeyboardButton("Сменить игру", callback_data="menu_change_game"),
        InlineKeyboardButton("🆔 Профиль", callback_data="menu_profile")
    )
    return keyboard

# ===================== Меню подсчёта =====================
def calc_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💰Посчитать ₸ в G", callback_data="calc_tenge_to_g"),
        InlineKeyboardButton("🌟Посчитать G в ₸", callback_data="calc_g_to_tenge"),
        InlineKeyboardButton("🏠Главное меню", callback_data="calc_back")
    )
    return keyboard

# ===================== Админ-панель =====================
def admin_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("⏳ Ожидание оплаты", callback_data="admin_pending"),
        InlineKeyboardButton("✅ Оплаченные", callback_data="admin_done")
    )
    return keyboard

