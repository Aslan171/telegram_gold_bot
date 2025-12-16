from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from decimal import Decimal, ROUND_DOWN
import os

from keyboards.calculate_keyboard import calc_main_kb
from states.user_states import CalculateState

router = Router()
RATE = Decimal(os.getenv("CURRENCY_RATE", "5.6"))

@router.message(F.text == "🔢Посчитать")
async def cmd_calc(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, выберите способ подсчёта на клавиатуре:", reply_markup=calc_main_kb())
    await state.set_state(CalculateState.mode)

@router.message(F.text == "Посчитать ₸ в G", CalculateState.mode)
async def tenge_to_g_prompt(message: Message, state: FSMContext):
    await message.answer("Введите сумму в ₸:", reply_markup=None)
    await state.set_state(CalculateState.amount)
    await state.update_data(mode="to_g")

@router.message(F.text == "Посчитать G в ₸", CalculateState.mode)
async def g_to_tenge_prompt(message: Message, state: FSMContext):
    await message.answer("Введите количество G:", reply_markup=None)
    await state.set_state(CalculateState.amount)
    await state.update_data(mode="to_tenge")

@router.message(CalculateState.amount)
async def calculate_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    mode = data.get("mode")
    text = message.text.strip().replace(",", ".")
    try:
        val = Decimal(text)
    except:
        await message.answer("Введите корректное число.")
        await state.clear()
        return

    if mode == "to_g":
        g = (val / RATE).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
        await message.answer(f"Результат: {g} G")
    else:
        tenge = (val * RATE).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
        await message.answer(f"Результат: {tenge} ₸")
    await state.clear()
