from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram.fsm.context import FSMContext
from decimal import Decimal, InvalidOperation

from states.user_states import DepositState
from keyboards.deposit_keyboard import (
    deposit_method_kb,
    deposit_confirm_kb,
    deposit_after_receipt_kb,
)
from keyboards.main_keyboard import build_main_kb
from db.db_utils import (
    ensure_user,
    create_deposit,
    attach_deposit_receipt,
)
from utils.image_utils import save_photo

router = Router()

RATE = Decimal(5.5)
MIN_DEPOSIT = Decimal(210.0)


# --- Начало депозита ---
@router.message(F.text == "💰Пополнить")
async def deposit_start(message: Message, state: FSMContext):
    await ensure_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name
    )

    await message.answer(
        f"🕹 Укажи сумму в ₸ (минимум {MIN_DEPOSIT}₸) для покупки Gold:",
        reply_markup=None
    )
    await state.set_state(DepositState.amount)


# --- Ввод суммы ---
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
        await message.answer("Введите корректную сумму (например: 560).")
        return

    if amount < MIN_DEPOSIT:
        await message.answer(
            f"‼️ Минимальная сумма пополнения - {MIN_DEPOSIT}₸"
        )
        return

    amount_gt = (amount / RATE).quantize(Decimal("0.00"))
    deposit_id = await create_deposit(
        message.from_user.id, amount, amount_gt
    )

    await state.update_data(
        deposit_id=deposit_id,
        amount=amount,
        amount_gt=amount_gt
    )

    await message.answer(
        f"📥 {amount}₸ = {amount_gt}G Голды\nВыберите способ оплаты:",
        reply_markup=deposit_method_kb()
    )


# --- Выбор метода оплаты ---
@router.callback_query(F.data.startswith("deposit_method:"))
async def handle_deposit_method(call: CallbackQuery, state: FSMContext):
    await call.answer()  # ✅ КРИТИЧЕСКИ ВАЖНО

    method = call.data.split(":")[1]
    data = await state.get_data()
    deposit_id = data.get("deposit_id")

    if not deposit_id:
        await call.message.answer(
            "❗ Произошла ошибка, начните снова.",
            reply_markup=build_main_kb()
        )
        await state.clear()
        return

    card_number = "4400-4303-3359-3462"
    amount = data.get("amount")

    await call.message.edit_text(
        f"🏦 Оплата: {method.capitalize()}\n"
        f"👤 Получатель: Аслан Ш\n"
        f"💳 Реквизиты: {card_number}\n"
        f"💰 Сумма: {amount}₸\n\n"
        f"✅ После оплаты нажмите «Я оплатил»",
        reply_markup=deposit_confirm_kb(amount, card_number)
    )

    await state.set_state(DepositState.waiting_receipt)


# --- Пользователь нажал «Я оплатил» ---
@router.callback_query(F.data == "deposit_paid")
async def deposit_paid(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.answer(
        "📸 Отправьте квитанцию об оплате (скриншот или фото)."
    )


# --- Пользователь прислал квитанцию ---
@router.message(DepositState.waiting_receipt, F.content_type == "photo")
async def receive_receipt(message: Message, state: FSMContext):
    data = await state.get_data()
    deposit_id = data.get("deposit_id")

    if not deposit_id:
        await message.answer(
            "❗ Произошла ошибка, начните снова.",
            reply_markup=build_main_kb()
        )
        await state.clear()
        return

    photo: PhotoSize = message.photo[-1]
    file_path = await save_photo(photo, message.from_user.id)
    await attach_deposit_receipt(deposit_id, file_path)

    await message.answer(
        "🔹 Квитанция получена. Ожидайте проверки админом.",
        reply_markup=deposit_after_receipt_kb()
    )

    await state.clear()


# --- Отмена ---
@router.callback_query(F.data == "deposit_cancel")
async def deposit_cancel(call: CallbackQuery, state: FSMContext):
    await call.answer()  # ✅ обязательно
    await state.clear()
    await call.message.edit_text(
        "❌ Пополнение отменено.",
        reply_markup=None
    )
