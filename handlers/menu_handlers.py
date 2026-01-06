from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

router = Router()


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="💰Deposit"),
                KeyboardButton(text="🔢Calculate"),
            ],
            [
                KeyboardButton(text="🌟Withdraw"),
                KeyboardButton(text="🆔Profile"),
            ],
            [
                KeyboardButton(text="📖Help & FAQ"),
                KeyboardButton(text="✅About Bot"),
            ],
        ],
    )


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🐉 Добро пожаловать в драконье хранилище Standoff2!\n\n"
        "Выбери действие:",
        reply_markup=main_menu_kb(),
    )


@router.message(F.text == "🏠Main Menu")
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🏠 Главное меню",
        reply_markup=main_menu_kb(),
    )
