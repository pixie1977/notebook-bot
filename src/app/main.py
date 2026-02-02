import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.config.config import TELEGRAM_TOKEN
from src.app.routers import start_router, weather_router, crypto_router, form_router, history_router


async def main():
    # Логирование
    logging.basicConfig(level=logging.INFO)

    # Создание бота и диспетчера
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключение роутеров
    dp.include_router(start_router)
    dp.include_router(weather_router)
    dp.include_router(crypto_router)
    dp.include_router(form_router)
    dp.include_router(history_router)

    # Запуск бота
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())