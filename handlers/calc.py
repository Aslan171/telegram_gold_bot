from aiogram import types
from utils.keyboards import main_menu_keyboard
from config import load_config

# Загружаем конфиг
config = load_config()
TENGE_TO_GOLD = config.rate_tenge_per_g  # теперь курс берётся из .env

async def вывести_handler(message: types.Message, user_balance: float):
    text = f"🍯Введите количество голды, которое желаете вывести 🔐На вашем балансе: {user_balance} G"
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🏠Главное меню", callback_data="main_menu"))
    await message.answer(text, reply_markup=keyboard)

async def проверить_вывод(message: types.Message, user_balance: float, сумма: float):
    if сумма > user_balance:
        await message.answer("У вас недостаточно G ❌")
    else:
        сумма_с_надбавкой = сумма * 1.2
        text = (
            f"Для вывода Голды выставите на рынок SM1014 'Serpent' за {сумма_с_надбавкой:.2f} G, "
            f"чтобы вам пришло {сумма} G 📸\n"
            "Затем нажмите 'Только мои запросы', сделайте скриншот и отправьте его в бота 🚫\n"
            "Пожалуйста, не меняйте аватарку и цену скина, пока идет вывод Голды."
        )
        # Добавляем клавиатуру с основными кнопками
        keyboard = main_menu_keyboard()
        await message.answer(text, reply_markup=keyboard)

async def пополнить_handler(message: types.Message, сумма_тенге: float):
    gold = сумма_тенге / TENGE_TO_GOLD
    text = f"📥 Пополнив на {сумма_тенге}₸ вы получаете {gold:.2f} G Голды 💳\nВыберите подходящий способ оплаты:"
    # Здесь можно добавить кнопки оплаты через InlineKeyboard
    await message.answer(text)

