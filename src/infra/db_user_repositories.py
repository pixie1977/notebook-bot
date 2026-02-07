"""
Реализации репозиториев пользователей: в памяти и через SQLAlchemy.
Связывает доменную модель User с ORM-моделью UserDbModel.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from .db_models import UserDbModel, Base
from ..core.models import User
from ..core.repositories import UserRepository


class InMemoryUserRepository(UserRepository):
    """
    Реализация репозитория пользователей в памяти.
    Подходит для тестирования и прототипирования.
    """

    def __init__(self) -> None:
        """
        Инициализирует хранилище пользователей.
        """
        self._items: dict[str, User] = {}

    def get(self, tg_id: str) -> Optional[User]:
        """
        Возвращает пользователя по его Telegram ID.

        :param tg_id: строковый идентификатор пользователя в Telegram.
        :return: объект User или None, если не найден.
        """
        return self._items.get(tg_id)

    def add(self, user: User) -> None:
        """
        Добавляет пользователя в хранилище.

        :param user: объект User для сохранения.
        """
        self._items[user.tg_id] = user  # Исправлено: ключ по tg_id, а не uid

    def list_by_id(self, tg_id: str) -> List[User]:
        """
        Возвращает всех пользователей с указанным Telegram ID.

        :param tg_id: строковый идентификатор пользователя.
        :return: список объектов User.
        """
        return [u for u in self._items.values() if u.tg_id == tg_id]


class SqlAlchemyUserRepository(UserRepository):
    """
    Реализация репозитория пользователей через SQLAlchemy.
    Сохраняет данные в базу данных.
    """

    def __init__(self, session: Session) -> None:
        """
        Инициализирует репозиторий с сессией БД.

        :param session: экземпляр SQLAlchemy Session.
        """
        self.session = session

    def get(self, tg_id: str) -> Optional[User]:
        """
        Получает последнего активного пользователя по Telegram ID.

        :param tg_id: строковый идентификатор пользователя.
        :return: объект User или None.
        """
        model = (
            self.session.query(UserDbModel)
            .filter(UserDbModel.tg_id == tg_id)
            .order_by(UserDbModel.modification_time.desc())
            .first()
        )
        if model:
            return User(
                uid=model.uid,
                tg_id=model.tg_id,
                name=model.name,
                age=model.age,
            )
        return None

    def add(self, user: User) -> None:
        """
        Сохраняет пользователя в БД.

        :param user: объект User для сохранения.
        """
        model = UserDbModel(
            tg_id=user.tg_id,
            name=user.name,
            age=user.age,
            modification_time=datetime.now(),
        )
        self.session.add(model)

    def list_by_id(self, tg_id: str) -> List[User]:
        """
        Возвращает всех пользователей с заданным Telegram ID.

        :param tg_id: строковый идентификатор пользователя.
        :return: список объектов User.
        """
        models = (
            self.session.query(UserDbModel)
            .filter(UserDbModel.tg_id == tg_id)
            .all()
        )
        return [
            User(
                uid=m.uid,
                tg_id=m.tg_id,
                name=m.name,
                age=m.age,
            ) for m in models
        ]

    def create_all_tables(self) -> None:
        """
        Создаёт все таблицы в базе данных (вызывать один раз при старте).
        """
        Base.metadata.create_all(bind=self.session.bind)