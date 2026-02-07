"""
Реализации репозиториев сообщений: в памяти и через SQLAlchemy.
Связывает доменную модель Message с ORM-моделью MessageDbModel.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from .db_models import Base, MessageDbModel
from ..core.models import Message
from ..core.repositories import MessageRepository


class InMemoryMessageRepository(MessageRepository):
    """
    Реализация репозитория сообщений в памяти.
    Подходит для тестирования и прототипирования.
    """

    def __init__(self) -> None:
        """
        Инициализирует хранилище сообщений.
        """
        self._items: dict[int, Message] = {}  # Ключ по uid (int), а не str

    def get(self, msg_id: str) -> Optional[Message]:
        """
        Возвращает сообщение по его внутреннему ID.

        :param msg_id: строковый идентификатор сообщения.
        :return: объект Message или None, если не найден.
        """
        try:
            uid = int(msg_id)
        except ValueError:
            return None
        return self._items.get(uid)

    def add(self, message: Message) -> None:
        """
        Добавляет сообщение в хранилище.

        :param message: объект Message для сохранения.
        """
        self._items[message.uid] = message

    def list_by_user_tg_id(self, tg_id: str, count: int = 5) -> List[Message]:
        """
        Возвращает последние N сообщений пользователя.

        :param tg_id: строковый идентификатор пользователя в Telegram.
        :param count: количество сообщений для получения (по умолчанию 5).
        :return: список объектов Message.
        """
        filtered = [msg for msg in self._items.values() if msg.tg_id == tg_id]
        # Сортировка по времени: новые первыми
        sorted_msgs = sorted(filtered, key=lambda m: m.created_at, reverse=True)
        return sorted_msgs[:count]


class SqlAlchemyMessageRepository(MessageRepository):
    """
    Реализация репозитория сообщений через SQLAlchemy.
    Сохраняет данные в базу данных.
    """

    def __init__(self, session: Session) -> None:
        """
        Инициализирует репозиторий с сессией БД.

        :param session: экземпляр SQLAlchemy Session.
        """
        self.session = session

    def get(self, msg_id: str) -> Optional[Message]:
        """
        Возвращает сообщение по его внутреннему ID.

        :param msg_id: строковый идентификатор сообщения.
        :return: объект Message или None.
        """
        try:
            uid = int(msg_id)
        except ValueError:
            return None

        model = self.session.query(MessageDbModel).filter_by(uid=uid).first()
        if model:
            return Message(
                uid=model.uid,
                tg_id=model.tg_id,
                text=model.text,
                created_at=model.created_at,
            )
        return None

    def add(self, message: Message) -> None:
        """
        Сохраняет сообщение в БД.

        :param message: объект Message для сохранения.
        """
        model = MessageDbModel(
            tg_id=message.tg_id,
            text=message.text,
            created_at=message.created_at,
        )
        self.session.add(model)

    def list_by_user_tg_id(self, tg_id: str, count: int = 5) -> List[Message]:
        """
        Возвращает последние N сообщений пользователя из БД.

        :param tg_id: строковый идентификатор пользователя.
        :param count: количество сообщений для получения.
        :return: список объектов Message.
        """
        models = (
            self.session.query(MessageDbModel)
            .filter(MessageDbModel.tg_id == tg_id)
            .order_by(MessageDbModel.created_at.desc())
            .limit(count)
            .all()
        )
        return [
            Message(
                uid=m.uid,
                tg_id=m.tg_id,
                text=m.text,
                created_at=m.created_at,
            ) for m in models
        ]

    def create_all_tables(self) -> None:
        """
        Создаёт все таблицы в базе данных (вызывать один раз при старте).
        """
        Base.metadata.create_all(bind=self.session.bind)