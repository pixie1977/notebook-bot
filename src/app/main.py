import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from uvicorn import Config, Server  # Импорт перемещён из функции

from src.app.web.app import create_app
from src.config.config import TELEGRAM_TOKEN, WEBHOOK_URL
from src.app.routers import (
    start_router,
    weather_router,
    crypto_router,
    form_router,
    history_router,
)


async def main():
    """
    Запуск бота в режиме webhook с использованием FastAPI и Uvicorn.
    Устанавливает вебхук, подключает роутеры и запускает HTTP-сервер для приёма обновлений.
    """
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    # Создание бота и диспетчера с FSM
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключение роутеров
    dp.include_router(start_router)
    dp.include_router(weather_router)
    dp.include_router(crypto_router)
    dp.include_router(form_router)
    dp.include_router(history_router)

    # Установка вебхука
    await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)

    # Создание и запуск FastAPI-приложения
    app = create_app(bot, dp)
    config = Config(app, host="0.0.0.0", port=8080, log_level="info")
    server = Server(config)

    logging.info("Bot is starting in webhook mode...")
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())