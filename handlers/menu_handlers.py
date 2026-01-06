from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import build_main_kb
from keyboards.deposit_keyboard import deposit_method_kb, deposit_after_receipt_kb, deposit_confirm_kb
from keyboards.withdraw_keyboard import withdraw_input_kb, withdraw_after_kb
from keyboards.calculate_keyboard import calc_main_kb
from states.user_states import DepositState, WithdrawState, CalculateState
from db.db_utils import get_balances, ensure_user

router = Router()


@router.message(F.text == "🏠Main Menu")
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    kb = build_main_kb()
    await message.answer("🏠 Main Menu", reply_markup=kb)


@router.message(F.text == "💰Deposit")
async def deposit_start(message: Message, state: FSMContext):
    await ensure_user(message.from_user.id)
    await state.set_state(DepositState.amount)
    # Используем новую клавиатуру выбора способа оплаты
    kb = deposit_method_kb()
    await message.answer("Select payment method:", reply_markup=kb)


@router.message(F.text == "🌟Withdraw")
async def withdraw_start(message: Message, state: FSMContext):
    await ensure_user(message.from_user.id)
    await state.set_state(WithdrawState.amount)
    kb = withdraw_input_kb()
    await message.answer("Enter amount of G to withdraw:", reply_markup=kb)


@router.message(F.text == "🔢Calculate")
async def calculate_start(message: Message, state: FSMContext):
    await state.set_state(CalculateState.mode)
    kb = calc_main_kb()
    await message.answer("Select conversion type:", reply_markup=kb)


@router.message(F.text == "🆔Profile")
async def profile(message: Message):
    balances = await get_balances(message.from_user.id)
    await message.answer(
        f"Your Profile:\nG: {balances['g_balance']}\nGT: {balances['gt_balance']}"
    )


@router.message(F.text == "✨Sell Gold")
async def sell_gold(message: Message):
    await message.answer("Sell Gold feature is under development.")


@router.message(F.text == "🕹️Change Game")
async def change_game(message: Message):
    await message.answer("Change Game feature is under development.")


@router.message(F.text == "📖Gold Withdrawal Rules")
async def rules_gold(message: Message):
    await message.answer("Gold withdrawal rules will be here...")


@router.message(F.text == "✅About Bot")
async def about_bot(message: Message):
    await message.answer("Bot information here...")


@router.message(F.text == "📖Help & FAQ")
async def help_bot(message: Message):
    await message.answer("FAQ and answers here...")

