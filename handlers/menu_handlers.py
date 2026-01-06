from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from db.db_utils import ensure_user, get_balances
from states.user_states import DepositState, WithdrawState, CalculateState
from keyboards.main_keyboard import build_main_kb

router = Router()


# ==========================
# /start — приветствие
# ==========================
@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    try:
        await ensure_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    except Exception as e:
        await message.answer("❌ Ошибка при инициализации пользователя.")
        return

    start_text = (
        "🐉 Добро пожаловать, воин Standoff2!\n\n"
        "Ты попал в драконье хранилище Голды 🏆 — здесь можно покупать и продавать игровую валюту за реальные тенге.\n\n"
        "💰 Преврати свои деньги в G Голды и усили своего персонажа!\n\n"
        "⚔️ Чтобы начать, выбери действие ниже:"
    )
    await message.answer(start_text, reply_markup=build_main_kb())


# ==========================
# Главное меню
# ==========================
@router.message(F.text == "🏠Главное меню", state="*")
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 Главное меню", reply_markup=build_main_kb())


# ==========================
# Пополнение
# ==========================
@router.message(F.text == "💰Пополнить", state="*")
async def deposit_start(message: Message, state: FSMContext):
    try:
        await ensure_user(message.from_user.id)
        await state.set_state(DepositState.amount)
        await message.answer(
            "🕹 Укажи сумму в ₸, на которую планируешь покупку — я сразу скажу, сколько Голды ты получишь!",
            reply_markup=None
        )
    except Exception:
        await message.answer("❌ Ошибка при инициализации депозита.")


# ==========================
# Вывод
# ==========================
@router.message(F.text == "🌟Вывести", state="*")
async def withdraw_start(message: Message, state: FSMContext):
    try:
        await ensure_user(message.from_user.id)
        await state.set_state(WithdrawState.amount)
        await message.answer("Введите сумму для вывода:", reply_markup=None)
    except Exception:
        await message.answer("❌ Ошибка при инициализации вывода.")


# ==========================
# Конвертация
# ==========================
@router.message(F.text == "🔢Посчитать", state="*")
async def calculate_start(message: Message, state: FSMContext):
    try:
        await state.set_state(CalculateState.mode)
        await message.answer("Выберите конвертацию:", reply_markup=None)
    except Exception:
        await message.answer("❌ Ошибка при запуске калькулятора.")


# ==========================
# Профиль
# ==========================
@router.message(F.text == "🆔Профиль", state="*")
async def profile(message: Message):
    try:
        balances = await get_balances(message.from_user.id)
        await message.answer(f"Ваш профиль:\nG: {balances.get('g_balance', 0)}\nGT: {balances.get('gt_balance', 0)}")
    except Exception:
        await message.answer("❌ Ошибка при загрузке профиля.")


# ==========================
# О боте
# ==========================
@router.message(F.text == "✅О боте", state="*")
async def about_bot(message: Message):
    await message.answer("Информация о боте...")


# ==========================
# Помощь
# ==========================
@router.message(F.text == "📖Помощь и ответы", state="*")
async def help_bot(message: Message):
    await message.answer("FAQ и ответы здесь...")


# ==========================
# Продажа Голды
# ==========================
@router.message(F.text == "✨Продать голду", state="*")
async def sell_gold(message: Message):
    await message.answer("Функция продажи Голды пока в разработке.")


# ==========================
# Сменить игру
# ==========================
@router.message(F.text == "🕹️Сменить игру", state="*")
async def change_game(message: Message):
    await message.answer("Функция смены игры пока в разработке.")


# ==========================
# Правила вывода
# ==========================
@router.message(F.text == "📖Правила вывода Gold", state="*")
async def rules_gold(message: Message):
    await message.answer("Правила вывода Голды будут здесь...")

