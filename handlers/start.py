from aiogram import Router, types
from utils.keyboards import calc_menu, main_menu
from config import RATE_TENGE_PER_G

router = Router()

# Старт кнопки "Посчитать"
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
        # далее нужно ловить текст пользователя и считать
        await callback.answer()
    elif data == "calc_g_to_tenge":
        await callback.message.answer("⚙️ Введите сумму в G для расчёта:")
        # далее ловим текст и считаем
        await callback.answer()
    elif data == "calc_back":
        await callback.message.answer(
            "🏠 Главное меню",
            reply_markup=main_menu()
        )
        await callback.answer()


