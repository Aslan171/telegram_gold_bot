from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    PhotoSize
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    InlineKeyboardBuilder
)

from decimal import Decimal, ROUND_DOWN, InvalidOperation
import os

from states.user_states import DepositState
from db.db_utils import ensure_user, create_deposit, attach_deposit_receipt, get_balances
from utils.image_utils import save_photo

router = Router()

RATE = Decimal(os.getenv("CURRENCY_RATE", "5.6"))
MIN_DEPOSIT = Decimal(os.getenv("MIN_DEPOSIT", "210"))

# =========================
# MAIN KEYBOARD (REPLY)
# =========================
def build_main_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="💰Deposit")
    kb.button(text="🌟Withdraw")
    kb.button(text="🔢Calculate")
    kb.button(text="🆔Profile")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# =========================
# /start
# =========================
@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await ensure_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name
    )

    text = (
        "🐉 <b>Добро пожаловать, воин Standoff2!</b>\n\n"
        "Ты вошёл в <b>Драконье хранилище Голды</b> 🏆\n\n"
        "🔥 Покупка и продажа G за реальные тенге\n"
        "⚡ Быстро • Честно • Безопасно\n\n"
        "⚔️ Выбери действие ниже:"
    )

    await message.answer(text, reply_markup=build_main_kb())

# =========================
# DEPOSIT — START
# =========================
@router.message(F.text == "💰Deposit")
async def deposit_start(message: Message, state: FSMContext):
    await state.set_state(DepositState.amount)
    await message.answer(
        "💰 Введите сумму в ₸ (тенге), которую хотите пополнить:",
        reply_markup=None
    )

# =========================
# DEPOSIT — AMOUNT
# =========================
@router.message(DepositState.amount)
async def deposit_amount(message: Message, state: FSMContext):
    text = message.text.replace(",", ".").strip()

    try:
        amount = Decimal(text)
    except InvalidOperation:
        await message.answer("❌ Введите корректное число (например 560)")
        return

    if amount < MIN_DEPOSIT:
        await message.answer(f"⚠️ Минимум: {MIN_DEPOSIT}₸")
        return

    amount_g = (amount / RATE).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
    deposit_id = await create_deposit(message.from_user.id, amount, amount_g)

    await state.update_data(
        deposit_id=deposit_id,
        amount=amount,
        amount_g=amount_g
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="🔴 Kaspi", callback_data="deposit_method:kaspi")
    kb.button(text="❌ Отмена", callback_data="deposit_cancel")
    kb.adjust(2)

    await message.answer(
        f"📥 Вы получите <b>{amount_g} G</b>\n"
        f"💳 Сумма к оплате: <b>{amount}₸</b>\n\n"
        "Выберите способ оплаты:",
        reply_markup=kb.as_markup()
    )

# =========================
# DEPOSIT — METHOD
# =========================
@router.callback_query(F.data.startswith("deposit_method:"))
async def deposit_method(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount = data.get("amount")

    if not amount:
        await call.message.answer("❌ Ошибка. Начните заново.")
        await state.clear()
        return

    card = "4400 4303 3359 3462"

    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Я оплатил", callback_data="deposit_confirm")
    kb.button(text="❌ Отмена", callback_data="deposit_cancel")
    kb.adjust(2)

    await call.message.edit_text(
        f"🏦 <b>Kaspi Bank</b>\n\n"
        f"👤 Получатель: <b>Аслан Ш</b>\n"
        f"💳 Карта: <code>{card}</code>\n"
        f"💰 Сумма: <b>{amount}₸</b>\n\n"
        "После оплаты нажмите кнопку ниже:",
        reply_markup=kb.as_markup()
    )

    await state.set_state(DepositState.waiting_receipt)

# =========================
# DEPOSIT — CONFIRM
# =========================
@router.callback_query(F.data == "deposit_confirm")
async def deposit_confirm(call: CallbackQuery):
    await call.message.answer(
        "📸 Отправьте скриншот квитанции об оплате."
    )

# =========================
# DEPOSIT — CANCEL
# =========================
@router.callback_query(F.data == "deposit_cancel")
async def deposit_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("❌ Пополнение отменено.")

# =========================
# DEPOSIT — RECEIPT PHOTO
# =========================
@router.message(DepositState.waiting_receipt, F.photo)
async def deposit_receipt(message: Message, state: FSMContext):
    data = await state.get_data()
    deposit_id = data.get("deposit_id")

    if not deposit_id:
        await message.answer("❌ Ошибка. Начните заново.")
        await state.clear()
        return

    photo: PhotoSize = message.photo[-1]
    path = await save_photo(photo, message.from_user.id)
    await attach_deposit_receipt(deposit_id, path)

    await message.answer(
        "✅ Квитанция получена.\n"
        "⏳ Ожидайте подтверждения администратором."
    )

    await state.clear()

# =========================
# PROFILE
# =========================
@router.message(F.text == "🆔Profile")
async def profile(message: Message):
    b = await get_balances(message.from_user.id)
    await message.answer(
        f"👤 <b>Ваш профиль</b>\n\n"
        f"💰 G: <b>{b['g_balance']}</b>\n"
        f"🏦 GT: <b>{b['gt_balance']}</b>"
    )
