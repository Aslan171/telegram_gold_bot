from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from decimal import Decimal, ROUND_HALF_UP
import os

from keyboards.withdraw_keyboard import withdraw_input_kb, withdraw_after_kb
from keyboards.main_keyboard import build_main_kb
from states.user_states import WithdrawState
from db.db_utils import ensure_user, get_balances, create_withdrawal

router = Router()
CURRENCY_RATE = Decimal(os.getenv("CURRENCY_RATE", "5.6"))
WITHDRAW_MULTIPLIER = Decimal(os.getenv("WITHDRAW_MULTIPLIER", "1.25"))


@router.message(F.text == "🌟Вывести")
async def cmd_withdraw(message: Message, state: FSMContext):
    await ensure_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    balances = await get_balances(message.from_user.id)
    g_balance = balances["g_balance"]
    kb = withdraw_input_kb()
    await message.answer(
        f"🍯Введите количество голды, которое желаете вывести\n🔐На вашем балансе: {g_balance} G",
        reply_markup=kb
    )
    await state.set_state(WithdrawState.amount)


@router.message(WithdrawState.amount)
async def handle_withdraw_amount(message: Message, state: FSMContext):
    text = message.text.strip().replace(",", ".")

    # Обработка кнопки "Назад"
    if text == "⬅Назад":
        await state.clear()
        await message.answer(
            "🏠 Главное меню\nДля удобства используйте клавиатуру бота.\n\n"
            "💰 Для оформления покупки перейдите в раздел «Пополнить баланс».",
            reply_markup=build_main_kb()
        )
        return

    try:
        amount = Decimal(text)
    except:
        await message.answer(
            "Пожалуйста, введите корректное число (например: 100). Или нажмите ⬅Назад.",
            reply_markup=withdraw_input_kb()
        )
        return

    balances = await get_balances(message.from_user.id)
    g_balance = balances["g_balance"]

    if amount > g_balance:
        await message.answer("Извините, у вас недостаточно средств", reply_markup=withdraw_input_kb())
        await state.clear()
        return

    # Рассчёт цены для выставления (округление до целого, математическое)
    price_listing = (amount * WITHDRAW_MULTIPLIER).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    # Создание заявки на вывод в БД (pending)
    withdraw_id = await create_withdrawal(message.from_user.id, amount, price_listing)

    text = (
        f"Для вывода Голды выставьте на рынок SM1014 «Serpent» за {price_listing} G, чтобы вам пришло {amount} G\n\n"
        "📸 Затем нажмите «Только мои запросы» (как показано на фотографии), сделайте скриншот и отправьте его в бота.\n\n"
        "🚫 Пожалуйста, не меняйте аватарку и цену скина, пока идёт вывод Голды.\nЕсли потребуется — мы обязательно сообщим."
    )
    await message.answer(text, reply_markup=withdraw_after_kb())
    await state.clear()
