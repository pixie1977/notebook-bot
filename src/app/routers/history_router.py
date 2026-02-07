from aiogram import Router, types
from aiogram.filters import Command

from src.infra.db_service import get_last_messages_by_user_tg_id, save_message


router = Router()


@router.message(Command("last"))
async def cmd_last(message: types.Message) -> None:
    """
    Обработчик команды /last.
    Отправляет пользователю последние 5 его сообщений из базы данных.
    """
    await message.answer("Последние 5 сообщений:")
    tg_id: str = str(message.from_user.id)
    last_messages = get_last_messages_by_user_tg_id(tg_id=tg_id)

    if not last_messages:
        await message.answer("У вас пока нет сохранённых сообщений.")
        return

    for msg in last_messages:
        await message.answer(msg.text)


@router.message()
async def save_user_message(message: types.Message) -> None:
    """
    Универсальный хендлер.
    Сохраняет текст входящего сообщения в БД.
    Должен быть последним в роутере.
    """
    tg_id: str = str(message.from_user.id)

    if message.text:
        save_message(tg_id=tg_id, text=message.text)