from aiogram import types
from fastapi import FastAPI


def create_app(bot, dp):
    app = FastAPI()

    @app.post("/api/webhook")
    async def webhook(update: dict):
        telegram_update = types.Update(**update)
        await dp.feed_update(bot, telegram_update)
        return {"status": "ok"}

    @app.get("/healthz")
    async def health_check():
        return {"status": "ok"}

    @app.on_event("startup")
    async def on_startup():
        # Можно добавить инициализацию БД и т.д.
        pass

    @app.on_event("shutdown")
    async def on_shutdown():
        await bot.session.close()

    return app