from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from decimal import Decimal, InvalidOperation

from states.user_states import CalculateState
from utils.calc_utils import tenge_to_gold, gold_to_tenge

router = Router()


# --- Клавиатуры ---
def calc_main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Посчитать ₸ в G"), KeyboardButton("Посчитать G в ₸")],
            [KeyboardButton("🏠Главное меню")]
        ],
        resize_keyboard=True
    )


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🏠Главное меню")]
        ],
        resize_keyboard=True
    )


# --- Выбор режима конвертации ---
@router.message(F.text == "🔢Посчитать")
async def calc_start(message: Message, state: FSMContext):
    await state.set_state(CalculateState.mode)
    await message.answer(
        "Выберите режим конвертации:",
        reply_markup=calc_main_kb()  # Новая клавиатура заменит старую
    )


# --- Обработка выбора режима ---
@router.message(CalculateState.mode)
async def choose_mode(message: Message, state: FSMContext):
    text = message.text.strip()
    if text == "Посчитать ₸ в G":
        await state.update_data(mode="to_g")
    elif text == "Посчитать G в ₸":
        await state.update_data(mode="to_tenge")
    elif text in ["🏠Главное меню", "⬅Назад"]:
        await state.clear()
        await message.answer("🏠 Главное меню", reply_markup=main_menu_kb())
        return
    else:
        await message.answer("Выберите корректный режим.", reply_markup=calc_main_kb())
        return

    await state.set_state(CalculateState.amount)
    await message.answer(
        "Введите сумму для конвертации:",
        reply_markup=main_menu_kb()  # Меняем клавиатуру на «Главное меню» пока пользователь вводит число
    )


# --- Обработка суммы ---
@router.message(CalculateState.amount)
async def calculate_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    mode = data.get("mode")
    text = message.text.strip().replace(",", ".")

    if text in ["🏠Главное меню", "⬅Назад"]:
        await state.clear()
        await message.answer("🏠 Главное меню", reply_markup=main_menu_kb())
        return

    try:
        amount = Decimal(text)
    except InvalidOperation:
        await message.answer("Введите корректное число.", reply_markup=main_menu_kb())
        return

    if amount < 0:
        await message.answer("Сумма не может быть отрицательной.", reply_markup=main_menu_kb())
        return

    if mode == "to_g":
        result = tenge_to_gold(float(amount))
        await message.answer(f"{amount} ₸ = {result} G", reply_markup=main_menu_kb())
    else:
        result = gold_to_tenge(float(amount))
        await message.answer(f"{amount} G = {result} ₸", reply_markup=main_menu_kb())

    await state.clear()
