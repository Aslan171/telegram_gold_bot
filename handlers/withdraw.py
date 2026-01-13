from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from decimal import Decimal, InvalidOperation

from states.user_states import WithdrawState
from keyboards.withdraw_keyboard import withdraw_input_kb, withdraw_after_kb
from keyboards.main_keyboard import build_main_kb
from db.db_utils import (
    ensure_user,
    create_withdrawal,
    attach_withdraw_screenshot
)
from utils.image_utils import save_photo

router = Router()

MIN_WITHDRAW_G = Decimal("1.00")


# ───────────────────────────────
# НАЧАЛО ВЫВОДА
# ───────────────────────────────
@router.message(F.text == "🌟Вывести")
async def withdraw_start(message: Message, state: FSMContext):
    await ensure_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name
    )

    await state.clear()
    await state.set_state(WithdrawState.amount)

    await message.answer(
        f"💰 Введите сумму Gold для вывода (минимум {MIN_WITHDRAW_G}G):",
        reply_markup=withdraw_input_kb()
    )


# ───────────────────────────────
# ВВОД СУММЫ
# ───────────────────────────────
@router.message(WithdrawState.amount, F.text)
async def withdraw_amount(message: Message, state: FSMContext):
    text = message.text.strip().replace(",", ".")

    if text in ("⬅Назад", "🏠Главное меню"):
        await state.clear()
        await message.answer("🏠 Главное меню", reply_markup=build_main_kb())
        return

    try:
        amount_g = Decimal(text)
    except InvalidOperation:
        await message.answer("❌ Введите корректное число (например 5.25)")
        return

    if amount_g < MIN_WITHDRAW_G:
        await message.answer(f"❌ Минимум для вывода — {MIN_WITHDRAW_G}G")
        return

    price = amount_g * Decimal("5.5")  # курс из env при желании

    withdraw_id = await create_withdrawal(
        user_id=message.from_user.id,
        amount_g=amount_g,
        price_listing=price
    )

    await state.update_data(withdraw_id=withdraw_id)

    await message.answer(
        f"✅ Заявка на вывод {amount_g}G создана.\n"
        "📸 Пришлите скриншот подтверждения:",
        reply_markup=None
    )


# ───────────────────────────────
# ПОЛУЧЕНИЕ СКРИНШОТА
# ───────────────────────────────
@router.message(WithdrawState.amount, F.photo)
async def withdraw_screenshot(message: Message, state: FSMContext):
    data = await state.get_data()
    withdraw_id = data.get("withdraw_id")

    if not withdraw_id:
        await state.clear()
        await message.answer("❌ Ошибка. Начните заново.", reply_markup=build_main_kb())
        return

    photo = message.photo[-1]
    file_path = await save_photo(photo, message.from_user.id)

    await attach_withdraw_screenshot(withdraw_id, file_path)

    await state.clear()
    await message.answer(
        "🕓 Скриншот получен. Ожидайте проверки.",
        reply_markup=withdraw_after_kb()
    )


# ───────────────────────────────
# ОТМЕНА
# ───────────────────────────────
@router.message(F.text == "⬅Назад")
async def withdraw_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Вывод отменён.", reply_markup=build_main_kb())