from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import build_main_kb
from db.db_utils import ensure_user

router = Router()

# ---------- /start ----------
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await ensure_user(message.from_user.id, message.from_user.username, message.from_user.full_name)

    await message.answer(
        "Привет! Добро пожаловать в DragonX GoldX 🐉",
        reply_markup=build_main_kb()
    )

# ---------- Главное меню (ГЛОБАЛЬНО) ----------
@router.message(F.text == "🏠Главное меню")
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🏠 Главное меню\nВыберите нужный раздел:",
        reply_markup=build_main_kb()
    )

# ---------- О боте ----------
@router.message(F.text == "✅О боте")
async def about_bot(message: Message):
    await message.answer(
        "🔴 Dragon Gold – Магазин выгодного доната!\n\n"
        "Мы гарантируем безопасность и быструю обработку заказов.",
        reply_markup=build_main_kb()
    )

# ---------- Помощь ----------
@router.message(F.text == "📖Помощь и ответы")
async def help_and_faq(message: Message):
    await message.answer(
        "📜 Часто задаваемые вопросы:\n\n"
        "1️⃣ Как оплатить?\n"
        "2️⃣ Безопасно ли?\n"
        "3️⃣ Сроки вывода?\n"
        "4️⃣ Сотрудничество\n",
        reply_markup=build_main_kb()
    )

# ---------- Заглушки ----------
@router.message(F.text.in_({
    "🆔Профиль",
    "✨Продать голду",
    "🕹️Сменить игру",
    "📖Правила вывода Gold"
}))
async def stub(message: Message):
    await message.answer("🚧 Раздел в разработке", reply_markup=build_main_kb())
