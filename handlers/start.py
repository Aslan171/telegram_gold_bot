from aiogram import Router, types
from utils.keyboards import main_menu, calc_menu
from config import load_config

router = Router()

# Загружаем конфиг
config = load_config()
RATE_TENGE_PER_G = config.rate_tenge_per_g  # курс для конвертации

# Хендлер на команду /start
@router.message(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Добро пожаловать в бота 😎\n"
        "Выберите действие на панели ниже ⬇️",
        reply_markup=main_menu()  # главная клавиатура с кнопками
    )

# Старт кнопки "Посчитать" (как отдельная команда)
async def calc_start(message: types.Message):
    await message.answer(
        "✨ Пожалуйста, выберите способ подсчёта на клавиатуре:",
        reply_markup=calc_menu()
    )

# Обработка кнопок конвертации
@router.callback_query(lambda c: c.data)
async def calc_handler(callback: types.CallbackQuery):
    data = callback.data

    if data == "calc_tenge_to_g":
        await callback.message.answer("🧾 Введите сумму в ₸ для расчёта:")
        await callback.answer()
    elif data == "calc_g_to_tenge":
        await callback.message.answer("⚙️ Введите сумму в G для расчёта:")
        await callback.answer()
    elif data == "calc_back":
        await callback.message.answer(
            "🏠 Главное меню",
            reply_markup=main_menu()
        )
        await callback.answer()





