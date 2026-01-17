from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from decimal import Decimal

# --- Выбор метода оплаты ---
def deposit_method_kb(methods: list[str] = None) -> InlineKeyboardMarkup:
    """
    Генерация клавиатуры выбора метода оплаты.
    Можно передать список методов, по умолчанию только Каспи.
    """
    if methods is None:
        methods = ["Каспи"]

    buttons = [
        InlineKeyboardButton(
            text=f"🔴 {method}",
            callback_data=f"deposit_method:{method.lower()}"
        ) for method in methods
    ]

    # Добавляем кнопку "Перейти назад"
    buttons.append(
        InlineKeyboardButton(text="⏪ Перейти назад", callback_data="deposit_cancel")
    )

    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(*buttons)
    return kb


# --- После отправки квитанции ---
def deposit_after_receipt_kb() -> InlineKeyboardMarkup:
    """
    Клавиатура после того, как пользователь отправил квитанцию.
    """
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(text="Проблема с оплатой", callback_data="deposit_problem"),
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="deposit_cancel")
    )
    return kb


# --- Подтверждение оплаты (после выбора метода) ---
def deposit_confirm_kb(amount: Decimal, card_number: str) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой "Я оплатил" и "Отмена".
    Параметр amount должен быть Decimal для точности.
    """
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(
            text=f"✅ Я оплатил {amount}₸",
            callback_data="deposit_paid"
        ),
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data="deposit_cancel"
        )
    )
    return kb
