from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from decimal import Decimal, ROUND_DOWN, InvalidOperation
import os

from keyboards.deposit_keyboard import deposit_payment_kb, deposit_after_receipt_kb
from keyboards.main_keyboard import build_main_kb
from states.user_states import DepositState
from db.db_utils import ensure_user, create_deposit, attach_deposit_receipt

router = Router()
RATE = Decimal(os.getenv("CURRENCY_RATE", "5.6"))
MIN_DEPOSIT = Decimal(os.getenv("MIN_DEPOSIT", "210.0"))

@router.message(F.text == "💰Пополнить")
async def cmd_deposit(message: Message, state: FSMContext):
    await ensure_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.answer(
        "🕹 Укажи сумму в ₸, на которую планируешь покупку — я сразу скажу, сколько Голды ты получишь!",
        reply_markup=None
    )
    await state.set_state(DepositState.amount)

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
        await state.clear()
        return

    amount_gt = (amount / RATE).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
    deposit_id = await create_deposit(message.from_user.id, amount, amount_gt)
    await state.update_data(deposit_id=deposit_id)

    await message.answer(
        f"📥 Пополнив на {amount}₸ вы получаете {amount_gt}G Голды\n\n💳 Выберите подходящий способ оплаты:",
        reply_markup=deposit_payment_kb()
    )

@router.message(F.text == "🔴Каспи")
async def handle_kaspi(message: Message, state: FSMContext):
    data = await state.get_data()
    deposit_id = data.get("deposit_id")
    if not deposit_id:
        await message.answer("❗ Произошла ошибка, начните снова.", reply_markup=build_main_kb())
        await state.clear()
        return

    await message.answer(
        "🏦 Банк для оплаты: 🔴 Каспи\n\n"
        "Просьба указывать сумму покупаемого товара и его название в комментариях перевода, это ускорит процесс проверки ❤️\n\n"
        "👤 Получатель: Аслан Ш\n🤩 Реквизиты: 4400-4303-3359-3462\n\n"
        "✅ После оплаты отправьте скриншот чека ⤵️",
        reply_markup=deposit_after_receipt_kb()
    )
    await state.set_state(DepositState.waiting_receipt)

@router.message(DepositState.waiting_receipt, F.content_type == "photo")
async def receive_receipt_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    deposit_id = data.get("deposit_id")
    if not deposit_id:
        await message.answer("❗ Произошла ошибка, начните снова.", reply_markup=build_main_kb())
        await state.clear()
        return

    file_id = message.photo[-1].file_id
    await attach_deposit_receipt(deposit_id, file_id)

    await message.answer(
        "🔹 «Подтверждаете ли вы, что предоставленный вами документ является квитанцией»?\n\n"
        "⚠️При отсутствии квитанции или неверном документе заявка не будет обработана вовремя.",
        reply_markup=None
    )

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Да подтверждаю"), KeyboardButton("🏠Главное меню"))
    await message.answer("Выберите действие:", reply_markup=kb)
    await state.clear()
