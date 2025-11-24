from aiogram import Router, types
from utils.keyboards import main_menu
from handlers.calc import calc_start
from handlers.profile import profile_start
from handlers.payments import withdraw_start, deposit_start

router = Router()

@router.callback_query(lambda c: c.data)
async def menu_handler(callback: types.CallbackQuery):
    data = callback.data

    if data == "menu_withdraw":
        await withdraw_start(callback.message)
    elif data == "menu_deposit":
        await deposit_start(callback.message)
    elif data == "menu_calc":
        await calc_start(callback.message)
    elif data == "menu_profile":
        await profile_start(callback.message)
    elif data == "menu_about":
        await callback.message.answer("ℹ️ Этот бот управляет балансом Gold / GT.")
    elif data == "menu_help":
        await callback.message.answer("❓ Если возникли вопросы, обратитесь к @YourSupport.")
    elif data == "menu_sell":
        await callback.message.answer("💰 Функция продажи голды в разработке.")
    elif data == "menu_change_game":
        await callback.message.answer("🎮 Функция смены игры в разработке.")
    else:
        await callback.message.answer("⚠️ Неизвестная команда.")

    # Отвечаем на callback, чтобы убрать «часики» в Telegram
    await callback.answer()


