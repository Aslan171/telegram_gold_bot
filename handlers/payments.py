from aiogram import Router, types
from utils.keyboards import main_menu
from services.db import get_user_by_tg_id, update_user_balance
from config import RATE_TENGE_PER_G

router = Router()

# Состояние пользователя для вывода / пополнения
user_state = {}

# ===================== Вывести Голду =====================
async def withdraw_start(message: types.Message):
    user = await get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("⚠️ Пользователь не найден.")
        return

    user_state[message.from_user.id] = "withdraw"
    await message.answer(
        f"🍯 Введите количество голды, которое желаете вывести\n"
        f"🔐 На вашем балансе: {user['game_balance']} G",
    reply_markup=None
    )

# Обработка текста для вывода
async def withdraw_text(message: types.Message):
    user_id = message.from_user.id
    if user_state.get(user_id) != "withdraw":
        return

    try:
        amount = float(message.text)
    except ValueError:
        await message.answer("⚠️ Введите число.")
        return

    user = await get_user_by_tg_id(user_id)
    if amount > user['game_balance']:
        await message.answer("У вас недостаточно G ❌")
        return

    total_price = amount * 1.2  # +20%
    await message.answer(
        f'Для вывода Голды выставьте на рынок SM1014 "Serpent" за {total_price:.2f} G, чтобы вам пришло {amount:.2f} G\n\n'
        "📸 Затем нажмите \"Только мои запросы\", сделайте скриншот и отправьте его боту\n"
        "🚫 Пожалуйста, не меняйте аватарку и цену скина, пока идет вывод Голды",
        reply_markup=main_menu()
    )
    del user_state[user_id]

# ===================== Пополнить баланс =====================
async def deposit_start(message: types.Message):
    user_state[message.from_user.id] = "deposit"
    await message.answer("🕹 Укажи сумму в ₸ , на которую планируешь покупку — я сразу скажу, сколько Голды ты получишь!")

async def deposit_text(message: types.Message):
    user_id = message.from_user.id
    if user_state.get(user_id) != "deposit":
        return

    try:
        amount = float(message.text)
    except ValueError:
        await message.answer("⚠️ Введите число.")
        return

    g_amount = amount / RATE_TENGE_PER_G
    await message.answer(
        f"📥 Пополнив на {amount:.0f}₸ вы получаете {g_amount:.2f} G Голды\n"
        "💳 Выберите подходящий способ оплаты:\n"
        "🔴 Каспи\n📖 Инструкция о покупке\n⏪ Перейти Назад",
        reply_markup=None
    )
    del user_state[user_id]


