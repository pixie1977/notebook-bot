from aiogram import Router, types
from aiogram.filters import Command

from src.infra.db_service import get_last_messages_by_user_tg_id, save_message

router = Router()

@router.message(Command("last"))
async def cmd_eth(message: types.Message):
    await message.answer("Последние 5 сообщений")
    tg_id: str = str(message.from_user.id)
    last_messages = get_last_messages_by_user_tg_id(tg_id=tg_id)
    for last_message in last_messages:
        await message.answer(last_message.text)


# этот обработчик ВСЕГДА должен быть последним
@router.message()
async def cmd_eth(message: types.Message):
    tg_id: str = str(message.from_user.id)
    # Получаем текст, если есть
    if message.text:
        save_message(tg_id=tg_id, text=message.text)