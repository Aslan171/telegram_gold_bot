from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.user_states import CalculateState
from utils.calc_utils import tenge_to_gold, gold_to_tenge

router = Router()

@router.message(CalculateState.mode)
async def choose_mode(message: Message, state: FSMContext):
    if message.text == "Calculate ₸ → G":
        await state.update_data(mode="to_g")
    elif message.text == "Calculate G → ₸":
        await state.update_data(mode="to_tenge")
    else:
        await message.answer("Choose a valid conversion mode.")
        return

    await state.set_state(CalculateState.amount)
    await message.answer("Enter the amount to convert:")

@router.message(CalculateState.amount)
async def calculate_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    mode = data.get("mode")
    try:
        amount = float(message.text)
        if mode == "to_g":
            result = tenge_to_gold(amount)
            await message.answer(f"{amount} ₸ = {result} G")
        else:
            result = gold_to_tenge(amount)
            await message.answer(f"{amount} G = {result} ₸")
        await state.clear()
    except ValueError:
        await message.answer("Enter a valid number.")
