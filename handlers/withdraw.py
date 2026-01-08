from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram.fsm.context import FSMContext
from decimal import Decimal, InvalidOperation

from states.user_states import WithdrawState
from keyboards.withdraw_keyboard import withdraw_input_kb, withdraw_after_kb
from keyboards.main_keyboard import build_main_kb
from db.db_utils import ensure_user, create_withdrawal, attach_withdraw_screenshot
from utils.image_utils import save_photo

router = Router()

MIN_WITHDRAW_G = Decimal("1.00")  # минимальная сумма вывода в Gold


# --- Начало вывода ---
@router.message(F.text == "🌟Вывести")
async def withdraw_start(message: Message, state: FSMContext):
    await ensure_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.answer(
        f"💰 Введите сумму Gold для вывода (минимум {MIN_WITHDRAW_G}G):",
        reply_markup=withdraw_input_kb()
    )
    await state.set_state(WithdrawState.amount)


# --- Ввод суммы ---
@router.message(WithdrawState.amount)
async def handle_withdraw_amount(message: Message, state: FSMContext):
    text = message.text.strip().replace(",", ".")
    if text in ["⬅Назад", "🏠Главное меню"]:
        await state.clear()
        await message.answer("🏠 Главное меню", reply_markup=build_main_kb())
        return

    try:
        amount_g = Decimal(text)
    except InvalidOperation:
        await message.answer("Введите корректное число Gold (например: 5.25).")
        return

    if amount_g < MIN_WITHDRAW_G:
        await message.answer(f"Минимальная сумма для вывода — {MIN_WITHDRAW_G}G")
        return

    # Создаем запись о выводе в БД
    price_listing = amount_g * Decimal("5.5")  # курс можно брать из .env
    withdraw_id = await create_withdrawal(message.from_user.id, amount_g, price_listing)
    await state.update_data(withdraw_id=withdraw_id, amount_g=amount_g)

    await message.answer(
        f"💰 Заявка на вывод {amount_g}G создана.\n"
        "📸 Пришлите скриншот перевода или подтверждения оплаты:",
        reply_markup=None
    )
    await state.set_state(WithdrawState.amount)  # остаёмся в том же стейте для скрина


# --- Пользователь прислал скриншот ---
@router.message(F.content_type == "photo", state=WithdrawState.amount)
async def receive_withdraw_screenshot(message: Message, state: FSMContext):
    data = await state.get_data()
    withdraw_id = data.get("withdraw_id")
    if not withdraw_id:
        await message.answer("❗ Произошла ошибка, начните снова.", reply_markup=build_main_kb())
        await state.clear()
        return

    photo: PhotoSize = message.photo[-1]
    file_path = await save_photo(photo, message.from_user.id)
    await attach_withdraw_screenshot(withdraw_id, file_path)

    await message.answer(
        "🔹 Скриншот получен. Ожидайте проверки админом.",
        reply_markup=withdraw_after_kb()
    )
    await state.clear()


# --- Отмена ---
@router.message(F.text == "⬅Назад")
async def withdraw_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Вывод отменен.", reply_markup=build_main_kb())
