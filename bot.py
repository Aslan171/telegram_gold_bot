import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_config
from handlers import start, menu, calc, profile, payments, admin


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="menu", description="Главное меню"),
        BotCommand(command="profile", description="Профиль"),
        BotCommand(command="calc", description="Калькулятор Голды"),
        BotCommand(command="payments", description="Пополнить баланс"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(level=logging.INFO)

    # Загружаем конфиг
    config = load_config()
    if not config.bot_token:
        raise ValueError("BOT_TOKEN не найден в .env")

    # Инициализация бота
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация хендлеров
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(calc.router)
    dp.include_router(profile.router)
    dp.include_router(payments.router)
    dp.include_router(admin.router)

    # Установка команд
    await set_commands(bot)

    # Запуск бота
    logging.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
