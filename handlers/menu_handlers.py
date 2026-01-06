from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import build_main_kb
from states.user_states import DepositState, WithdrawState, CalculateState
from db.db_utils import ensure_user, get_balances

router = Router()

# ==========================
# /start — Драконий привет
# ==========================
@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await ensure_user(message.from_user.id, message.from_user.username, message.from_user.full_name)

    start_text = (
        "🐉 **Добро пожаловать, воин Standoff2!**\n\n"
        "Ты попал в драконье хранилище Голды 🏆 — здесь можно покупать и продавать игровую валюту за реальные тенге.\n\n"
        "💰 Преврати свои деньги в G Голды и усили своего персонажа!\n\n"
        "⚔️ Чтобы начать, выбери действие ниже:"
    )

    kb = build_main_kb()
    await message.answer(start_text, reply_markup=kb)

# ==========================
# Main Menu — кнопка меню
# ==========================
@router.message(F.text == "🏠Main Menu", state="*")
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    kb = build_main_kb()
    await message.answer("🏠 Главное меню", reply_markup=kb)

# ==========================
# Deposit — кнопка пополнения
# ==========================
@router.message(F.text == "💰Deposit", state="*")
async def deposit_start(message: Message, state: FSMContext):
    await ensure_user(message.from_user.id)
    await state.set_state(DepositState.amount)
    await message.answer(
        "🕹 Укажи сумму в ₸, на которую планируешь покупку — я сразу скажу, сколько Голды ты получишь!",
        reply_markup=None
    )

# ==========================
# Withdraw — кнопка вывода
# ==========================
@router.message(F.text == "🌟Withdraw", state="*")
async def withdraw_start(message: Message, state: FSMContext):
    await ensure_user(message.from_user.id)
    await state.set_state(WithdrawState.amount)
    await message.answer(
        "Введите сумму для вывода:",
        reply_markup=None
    )

# ==========================
# Calculate — кнопка конвертации
# ==========================
@router.message(F.text == "🔢Calculate", state="*")
async def calculate_start(message: Message, state: FSMContext):
    await state.set_state(CalculateState.mode)
    await message.answer(
        "Выберите конвертацию:",
        reply_markup=None
    )

# ==========================
# Profile — кнопка профиля
# ==========================
@router.message(F.text == "🆔Profile", state="*")
async def profile(message: Message):
    balances = await get_balances(message.from_user.id)
    await message.answer(
        f"Ваш профиль:\nG: {balances['g_balance']}\nGT: {balances['gt_balance']}"
    )

# ==========================
# Help & FAQ
# ==========================
@router.message(F.text == "📖Help & FAQ", state="*")
async def help_bot(message: Message):
    await message.answer("FAQ и ответы здесь...")

# ==========================
# About Bot
# ==========================
@router.message(F.text == "✅About Bot", state="*")
async def about_bot(message: Message):
    await message.answer("Информация о боте...")

# ==========================
# Sell Gold — заглушка
# ==========================
@router.message(F.text == "✨Sell Gold", state="*")
async def sell_gold(message: Message):
    await message.answer("Функция продажи Голды пока в разработке.")

# ==========================
# Change Game — заглушка
# ==========================
@router.message(F.text == "🕹️Change Game", state="*")
async def change_game(message: Message):
    await message.answer("Функция смены игры пока в разработке.")

# ==========================
# Gold Withdrawal Rules — заглушка
# ==========================
@router.message(F.text == "📖Gold Withdrawal Rules", state="*")
async def rules_gold(message: Message):
    await message.answer("Правила вывода Голды будут здесь...")
