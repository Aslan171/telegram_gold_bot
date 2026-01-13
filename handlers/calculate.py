from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from decimal import Decimal, InvalidOperation

from states.user_states import CalculateState
from keyboards.calculate_keyboard import calc_main_kb
from utils.calc_utils import tenge_to_gold, gold_to_tenge

router = Router()


# --- Выбор режима конвертации ---
@router.message(F.text == "🔢Посчитать")
async def calc_start(message: Message, state: FSMContext):
    await state.set_state(CalculateState.mode)
    await message.answer(
        "Выберите режим конвертации:",
        reply_markup=calc_main_kb()
    )


# --- Обработка выбора режима ---
@router.message(CalculateState.mode)
async def choose_mode(message: Message, state: FSMContext):
    text = message.text.strip()
    if text == "Посчитать ₸ в G":
        await state.update_data(mode="to_g")
    elif text == "Посчитать G в ₸":
        await state.update_data(mode="to_tenge")
    elif text in ["🏠Главное меню", "⬅Назад"]:
        await state.clear()
        await message.answer("🏠 Главное меню", reply_markup=calc_main_kb())
        return
    else:
        await message.answer("Выберите корректный режим.")
        return

    await state.set_state(CalculateState.amount)
    await message.answer("Введите сумму для конвертации:")


# --- Обработка суммы ---
@router.message(CalculateState.amount)
async def calculate_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    mode = data.get("mode")
    text = message.text.strip().replace(",", ".")

    if text in ["🏠Главное меню", "⬅Назад"]:
        await state.clear()
        await message.answer("🏠 Главное меню", reply_markup=calc_main_kb())
        return

    try:
        amount = Decimal(text)
    except InvalidOperation:
        await message.answer("Введите корректное число.")
        return

    if amount < 0:
        await message.answer("Сумма не может быть отрицательной.")
        return

    if mode == "to_g":
        result = tenge_to_gold(float(amount))
        await message.answer(f"{amount} ₸ = {result} G")
    else:
        result = gold_to_tenge(float(amount))
        await message.answer(f"{amount} G = {result} ₸")

    await state.clear()
