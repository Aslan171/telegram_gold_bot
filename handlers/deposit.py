from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram import Bot
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

import os

router = Router()

# Получаем список админов из переменных окружения
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

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
    # print("[DEBUG] handle_deposit_method вызван")
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

    try:
        await call.message.edit_text(
            f"🏦 Оплата: {method.capitalize()}\n"
            f"👤 Получатель: Аслан Ш\n"
            f"💳 Реквизиты: {card_number}\n"
            f"💰 Сумма: {amount}₸\n\n"
            f"✅ После оплаты нажмите «Я оплатил»",
            reply_markup=deposit_confirm_kb(amount, card_number)
        )
    except Exception as e:
        print(f"[deposit] Ошибка при edit_text: {e}")
        await call.message.answer("Произошла ошибка при отображении реквизитов. Попробуйте ещё раз или обратитесь к администратору.")
        await call.message.answer(str(e))

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
    print("[DEBUG] receive_receipt вызван")
    await message.answer("[DEBUG] receive_receipt вызван")
    try:
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
        file_id = photo.file_id
        await attach_deposit_receipt(deposit_id, file_id)

        # Получаем сумму и user_id для админов
        amount = data.get("amount")
        user_id = message.from_user.id
        await send_receipt_to_admins(message.bot, file_id, amount, user_id, deposit_id)

        await message.answer(
            "🔹 Квитанция получена. Ожидайте проверки админом.",
            reply_markup=deposit_after_receipt_kb()
        )

        await state.clear()
    except Exception as e:
        print(f"[deposit] Ошибка в receive_receipt: {e}")
        await message.answer(f"Ошибка при обработке квитанции: {e}")

# Отправка квитанции и информации админам
async def send_receipt_to_admins(bot: Bot, file_id: str, amount, user_id, deposit_id):
    from keyboards.admin_keyboard import notification_kb
    text = (
        f"💸 Новый депозит на проверку!\n"
        f"Сумма: {amount}₸\n"
        f"User ID: {user_id}\n"
        f"Deposit ID: {deposit_id}"
    )
    kb = notification_kb(deposit_id, "deposit")
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_photo(admin_id, file_id, caption=text, reply_markup=kb)
        except Exception as e:
            print(f"[deposit] Не удалось отправить квитанцию админу {admin_id}: {e}")

# --- Отмена ---
@router.callback_query(F.data == "deposit_cancel")
async def deposit_cancel(call: CallbackQuery, state: FSMContext):
    await call.answer()  # ✅ обязательно
    await state.clear()
    await call.message.edit_text(
        "❌ Пополнение отменено.",
        reply_markup=None
    )

