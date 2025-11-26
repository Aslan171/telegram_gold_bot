from aiogram import Router, types
from utils.keyboards import main_menu, calc_menu
from config import load_config

router = Router()

# Загружаем конфиг
config = load_config()
RATE_TENGE_PER_G = config.rate_tenge_per_g  # курс для конвертации


# =====================  /start  =====================
@router.message(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Добро пожаловать в бота 😎\n"
        "Выберите действие на панели ниже ⬇️",
        reply_markup=main_menu()
    )


# =====================  ГЛАВНОЕ МЕНЮ  =====================
@router.callback_query(lambda c: c.data and c.data.startswith("menu_"))
async def menu_handler(callback: types.CallbackQuery):
    action = callback.data

    if action == "menu_calc":
        await callback.message.answer(
            "💱 Выберите способ подсчёта:",
            reply_markup=calc_menu()
        )

    elif action == "menu_withdraw":
        await callback.message.answer("🔻 Вы выбрали вывод. (логика позже)")

    elif action == "menu_deposit":
        await callback.message.answer("🔼 Вы выбрали пополнение.")

    elif action == "menu_about":
        await callback.message.answer("ℹ️ О боте...")

    elif action == "menu_help":
        await callback.message.answer("❓ Помощь...")

    elif action == "menu_sell":
        await callback.message.answer("💸 Продажа... позже.")

    elif action == "menu_change_game":
        await callback.message.answer("🎮 Выбор игры позже.")

    elif action == "menu_profile":
        await callback.message.answer("🆔 Профиль будет позже.")

    await callback.answer()


# =====================  КОНВЕРТАЦИЯ  =====================
@router.callback_query(lambda c: c.data and c.data.startswith("calc_"))
async def calc_handler(callback: types.CallbackQuery):
    data = callback.data

    if data == "calc_tenge_to_g":
        await callback.message.answer("🧾 Введите сумму в ₸ для расчёта:")

    elif data == "calc_g_to_tenge":
        await callback.message.answer("⚙️ Введите сумму в G для расчёта:")

    elif data == "calc_back":
        await callback.message.answer(
            "🏠 Главное меню",
            reply_markup=main_menu()
        )

    await callback.answer()






