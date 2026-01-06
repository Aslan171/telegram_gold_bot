from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, PhotoSize
from aiogram.fsm.context import FSMContext
from decimal import Decimal, ROUND_DOWN, InvalidOperation
import os

from states.user_states import DepositState, WithdrawState, CalculateState
from db.db_utils import ensure_user, create_deposit, attach_deposit_receipt, get_balances
from keyboards.main_keyboard import build_main_kb
from utils.image_utils import save_photo

router = Router()

RATE = Decimal(os.getenv("CURRENCY_RATE", "5.6"))
MIN_DEPOSIT = Decimal(os.getenv("MIN_DEPOSIT", "210.0"))

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
# Menu — Главные кнопки
# ==========================
@router.message(F.text == "🏠Main Menu")
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    kb = build_main_kb()
    await message.answer("🏠 Main Menu", reply_markup=kb)

# ==========================
# Deposit — начало
# ==========================
@router.message(F.text == "💰Deposit")
async def deposit_start(message: Message, state: FSMContext):
    await ensure_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await state.set_state(DepositState.amount)
    await message.answer(
        "🕹 Укажи сумму в ₸, на которую планируешь покупку — я сразу скажу, сколько Голды ты получишь!",
        reply_markup=None
    )

# Ввод суммы депозита
@router.message(DepositState.amount)
async def handle_deposit_amount(message: Message, state: FSMContext):
    text = message.text.strip().replace(",", ".")
    if text in ["⏪Перейти назад", "🏠Главное меню"]:
        await state.clear()
        await message.answer("🏠 Главное меню", reply_markup=build_main_kb())
        return

    try:
        amount = Decimal(text)
    except InvalidOperation:
        await message.answer("Введите корректную сумму в тенге (например: 560).", reply_markup=None)
        return

    if amount < MIN_DEPOSIT:
        await message.answer(f"‼️ Минимальная сумма пополнения - {MIN_DEPOSIT}₸", reply_markup=None)
        return

    amount_gt = (amount / RATE).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
    deposit_id = await create_deposit(message.from_user.id, amount, amount_gt)
    await state.update_data(deposit_id=deposit_id, amount=amount, amount_gt=amount_gt)

    # Inline кнопки выбора метода оплаты
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(text="🔴Каспи", callback_data="deposit_method:kaspi"),
        InlineKeyboardButton(text="⏪Перейти назад", callback_data="deposit_cancel")
    )

    await message.answer(
        f"📥 Пополнив на {amount}₸ вы получаете {amount_gt}G Голды\n\n"
        "💳 Выберите способ оплаты:",
        reply_markup=kb
    )

# ==========================
# Callback — выбор метода оплаты
# ==========================
@router.callback_query(F.data.startswith("deposit_method:"))
async def handle_deposit_method(call: CallbackQuery, state: FSMContext):
    method = call.data.split(":")[1]
    data = await state.get_data()
    deposit_id = data.get("deposit_id")
    amount = data.get("amount")

    if not deposit_id:
        await call.message.answer("❗ Произошла ошибка, начните снова.", reply_markup=build_main_kb())
        await state.clear()
        return

    card_number = "4400-4303-3359-3462"
    
    # Inline кнопка подтверждения оплаты
    confirm_kb = InlineKeyboardMarkup(row_width=2)
    confirm_kb.add(
        InlineKeyboardButton(text="✅ Я оплатил", callback_data="deposit_confirm"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="deposit_cancel")
    )

    await call.message.edit_text(
        f"🏦 Банк для оплаты: 🔴 {method.capitalize()}\n"
        f"👤 Получатель: Аслан Ш\n"
        f"💳 Реквизиты: {card_number}\n"
        f"💰 Сумма: {amount}₸\n\n"
        f"После оплаты нажмите кнопку 'Я оплатил'",
        reply_markup=confirm_kb
    )
    await state.set_state(DepositState.waiting_receipt)

# ==========================
# Callback — отмена депозита
# ==========================
@router.callback_query(F.data == "deposit_cancel")
async def deposit_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("❌ Пополнение отменено.", reply_markup=None)

# ==========================
# Пользователь прислал фото квитанции
# ==========================
@router.message(DepositState.waiting_receipt, F.content_type == "photo")
async def receive_receipt(message: Message, state: FSMContext):
    data = await state.get_data()
    deposit_id = data.get("deposit_id")
    if not deposit_id:
        await message.answer("❗ Произошла ошибка, начните снова.", reply_markup=build_main_kb())
        await state.clear()
        return

    photo: PhotoSize = message.photo[-1]
    file_path = await save_photo(photo, message.from_user.id)
    await attach_deposit_receipt(deposit_id, file_path)

    await message.answer(
        "🔹 Квитанция получена. Ожидайте проверки админом.",
        reply_markup=None
    )
    await state.clear()

# ==========================
# Withdraw — пример
# ==========================
@router.message(F.text == "🌟Withdraw")
async def withdraw_start(message: Message, state: FSMContext):
    await ensure_user(message.from_user.id)
    await state.set_state(WithdrawState.amount)
    await message.answer("Введите сумму для вывода:", reply_markup=None)

# ==========================
# Calculate — пример
# ==========================
@router.message(F.text == "🔢Calculate")
async def calculate_start(message: Message, state: FSMContext):
    await state.set_state(CalculateState.mode)
    await message.answer("Выберите конвертацию:", reply_markup=None)

# ==========================
# Profile, Help, About
# ==========================
@router.message(F.text == "🆔Profile")
async def profile(message: Message):
    balances = await get_balances(message.from_user.id)
    await message.answer(f"Ваш профиль:\nG: {balances['g_balance']}\nGT: {balances['gt_balance']}")

@router.message(F.text == "📖Help & FAQ")
async def help_bot(message: Message):
    await message.answer("FAQ и ответы здесь...")

@router.message(F.text == "✅About Bot")
async def about_bot(message: Message):
    await message.answer("Информация о боте...")
