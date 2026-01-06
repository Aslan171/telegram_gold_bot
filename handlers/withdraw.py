from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.user_states import WithdrawState
from db.db_utils import create_withdrawal, get_balances
from keyboards.withdraw_keyboard import withdraw_after_kb, withdraw_input_kb

router = Router()

@router.message(WithdrawState.amount)
async def withdraw_amount(message: Message, state: FSMContext):
    if message.text in ["⬅Back", "🏠Main Menu"]:
        await state.clear()
        await message.answer("Returning to menu.", reply_markup=None)
        return

    try:
        amount = float(message.text)
        balances = await get_balances(message.from_user.id)
        if balances["g_balance"] < amount:
            await message.answer("Insufficient G balance.")
            return
        withdraw_id = await create_withdrawal(
            message.from_user.id,
            amount_g=amount,
            price_listing=amount*5.5
        )
        kb = withdraw_after_kb()
        await message.answer(f"Withdrawal #{withdraw_id} created.", reply_markup=kb)
        await state.clear()
    except ValueError:
        await message.answer("Enter a valid number.")
