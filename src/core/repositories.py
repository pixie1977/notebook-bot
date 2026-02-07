"""
Модуль, определяющий порты репозиториев с использованием Protocol.
Служит абстракцией для взаимодействия с различными реализациями хранилищ (БД, память и т.д.).
"""
from __future__ import annotations
from typing import Protocol, Optional, List

from .models import User
from .models import Message


class UserRepository(Protocol):
    """
    Протокол для репозитория пользователей.
    Определяет контракт для всех реализаций.
    """

    def get(self, user_id: str) -> Optional[User]:
        """
        Получает пользователя по его внутреннему ID.

        :param user_id: строковый идентификатор пользователя.
        :return: объект User или None, если не найден.
        """
        ...

    def add(self, user: User) -> None:
        """
        Добавляет нового пользователя в хранилище.

        :param user: объект User для сохранения.
        """
        ...

    def list_by_id(self, tg_id: str) -> List[User]:
        """
        Возвращает список пользователей по их Telegram ID.

        :param tg_id: строковый идентификатор пользователя в Telegram.
        :return: список объектов User.
        """
        ...


class MessageRepository(Protocol):
    """
    Протокол для репозитория сообщений.
    Определяет контракт для всех реализаций.
    """

    def get(self, msg_id: str) -> Optional[Message]:
        """
        Получает сообщение по его внутреннему ID.

        :param msg_id: строковый идентификатор сообщения.
        :return: объект Message или None, если не найден.
        """
        ...

    def add(self, message: Message) -> None:
        """
        Добавляет новое сообщение в хранилище.

        :param message: объект Message для сохранения.
        """
        ...

    def list_by_user_tg_id(self, tg_id: str, count: int = 5) -> List[Message]:
        """
        Возвращает последние N сообщений пользователя.

        :param tg_id: строковый идентификатор пользователя в Telegram.
        :param count: количество последних сообщений (по умолчанию 5).
        :return: список объектов Message.
        """
        ...