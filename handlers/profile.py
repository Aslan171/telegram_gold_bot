from aiogram import Router, types
from utils.keyboards import main_menu
from services.db import get_user_by_tg_id

router = Router()

async def profile_start(message: types.Message):
    user = await get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("⚠️ Пользователь не найден.")
        return

    text = (
        f"🥇 Никнейм: @{user['username']} ({user['id']})\n\n"
        f"💰 Баланс: {user['balance']} GT\n"
        f"💰 Игровой баланс: {user['game_balance']} G\n\n"
        f"💵 Сумма заказов: {user['total_paid']} ₸\n\n"
        f"📰 Дата регистрации: {user['reg_date']}"
    )

    await message.answer(text, reply_markup=main_menu())

