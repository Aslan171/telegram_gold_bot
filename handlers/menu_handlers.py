from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import build_main_kb
from states.user_states import DepositState, WithdrawState, CalculateState
from db.db_utils import ensure_user, get_balances

router = Router()

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
        "🔥 Покупка и продажа Gold за тенге\n"
        "⚡ Быстро • Честно • Безопасно\n\n"
        "⚔️ Выбери действие ниже:"
    )

    await message.answer(text, reply_markup=build_main_kb())


# =========================
# Главное меню
# =========================
@router.message(F.text == "🏠Главное меню", state="*")
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 Главное меню", reply_markup=build_main_kb())


# =========================
# Пополнить
# =========================
@router.message(F.text == "💰Пополнить", state="*")
async def deposit_start(message: Message, state: FSMContext):
    await state.set_state(DepositState.amount)
    await message.answer(
        "💰 Введите сумму в ₸, на которую хотите купить Gold:",
        reply_markup=None
    )


# =========================
# Вывести
# =========================
@router.message(F.text == "🌟Вывести", state="*")
async def withdraw_start(message: Message, state: FSMContext):
    await state.set_state(WithdrawState.amount)
    await message.answer(
        "🌟 Введите сумму Gold для вывода:",
        reply_markup=None
    )


# =========================
# Посчитать
# =========================
@router.message(F.text == "🔢Посчитать", state="*")
async def calculate_start(message: Message, state: FSMContext):
    await state.set_state(CalculateState.mode)
    await message.answer(
        "🔢 Выберите тип конвертации:",
        reply_markup=None
    )


# =========================
# Профиль
# =========================
@router.message(F.text == "🆔Профиль", state="*")
async def profile(message: Message):
    balances = await get_balances(message.from_user.id)
    await message.answer(
        f"👤 <b>Ваш профиль</b>\n\n"
        f"💰 Gold: <b>{balances['g_balance']}</b>\n"
        f"🏦 GT: <b>{balances['gt_balance']}</b>"
    )


# =========================
# О боте
# =========================
@router.message(F.text == "✅О боте", state="*")
async def about_bot(message: Message):
    await message.answer(
        "🐉 <b>DragonX Gold</b>\n\n"
        "Сервис покупки и продажи Gold для Standoff2.\n"
        "Безопасно. Быстро. Надёжно."
    )


# =========================
# Помощь
# =========================
@router.message(F.text == "📖Помощь и ответы", state="*")
async def help_bot(message: Message):
    await message.answer(
        "📖 <b>Помощь</b>\n\n"
        "1️⃣ Выберите действие в меню\n"
        "2️⃣ Следуйте инструкциям бота\n"
        "3️⃣ При проблемах — напишите администратору"
    )


# =========================
# Продать голду (заглушка)
# =========================
@router.message(F.text == "✨Продать голду", state="*")
async def sell_gold(message: Message):
    await message.answer("✨ Продажа Gold скоро будет доступна.")


# =========================
# Сменить игру (заглушка)
# =========================
@router.message(F.text == "🕹️Сменить игру", state="*")
async def change_game(message: Message):
    await message.answer("🕹️ Смена игры в разработке.")


# =========================
# Правила вывода
# =========================
@router.message(F.text == "📖Правила вывода Gold", state="*")
async def rules_gold(message: Message):
    await message.answer(
        "📖 <b>Правила вывода Gold</b>\n\n"
        "• Минимальная сумма — зависит от курса\n"
        "• Проверка администратором\n"
        "• Вывод только после подтверждения"
    )
