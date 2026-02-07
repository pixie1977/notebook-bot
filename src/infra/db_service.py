"""
Сервисный слой для работы с пользователями и сообщениями.
Предоставляет функции высокого уровня для сохранения и получения данных через репозитории.
"""
from datetime import datetime
from typing import List

from src.core.models import User, Message
from src.infra.database import get_db_session
from src.infra.db_message_repositories import SqlAlchemyMessageRepository
from src.infra.db_user_repositories import SqlAlchemyUserRepository


def save_user(tg_id: str, name: str, age: int) -> User:
    """
    Сохраняет или обновляет пользователя в базе данных.

    :param tg_id: строковый идентификатор пользователя в Telegram.
    :param name: имя пользователя.
    :param age: возраст пользователя.
    :return: сохранённый объект User.
    """
    with get_db_session() as session:
        repo = SqlAlchemyUserRepository(session=session)
        user = repo.get(tg_id)

        if user is None:
            user = User(tg_id=tg_id, name=name, age=age)
        else:
            user.name = name
            user.age = age

        repo.add(user)
        session.commit()
        return repo.get(tg_id)


def save_message(tg_id: str, text: str) -> Message:
    """
    Сохраняет новое сообщение в базу данных.

    :param tg_id: строковый идентификатор отправителя.
    :param text: текст сообщения.
    :return: сохранённый объект Message.
    """
    with get_db_session() as session:
        repo = SqlAlchemyMessageRepository(session=session)
        message = Message(
            tg_id=tg_id,
            text=text,
            created_at=datetime.now(),
        )
        repo.add(message)
        session.commit()
        return message


def get_last_messages_by_user_tg_id(tg_id: str, count: int = 5) -> List[Message]:
    """
    Возвращает последние N сообщений пользователя из базы данных.

    :param tg_id: строковый идентификатор пользователя в Telegram.
    :param count: количество сообщений для получения (по умолчанию 5).
    :return: список объектов Message.
    """
    with get_db_session() as session:
        repo = SqlAlchemyMessageRepository(session=session)
        messages = repo.list_by_user_tg_id(tg_id, count)
        return messages[:count]