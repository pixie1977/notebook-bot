from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from .db_models import UserDbModel, Base
from ..core.models import User
from ..core.repositories import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._items: dict[str, User] = {}

    def get(self, id: str) -> Optional[User]:
        return self._items.get(id)

    def add(self, user: User) -> None:
        self._items[user.uid] = user

    def list_by_id(self, tg_id: str) -> List[User]:
        return [r for r in self._items.values() if r.tg_id == tg_id]


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, tg_id: str) -> Optional[User]:
        model = (
            self.session.query(UserDbModel)
            .filter(UserDbModel.tg_id == tg_id)
            .order_by(UserDbModel.modification_time.desc())  # сортировка по времени (новые первыми)
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
        model = UserDbModel(
            tg_id=user.tg_id,
            name=user.name,
            age=user.age,
            modification_time=datetime.now(),
        )
        self.session.add(model)

    def list_by_id(self, tg_id: str) -> List[User]:
        models = (self.session.query(UserDbModel)
                  .filter(UserDbModel.tg_id == tg_id)
                  .all())
        return [
            User(
                uid=m.uid,
                tg_id=m.tg_id,
                name=m.name,
                age=m.age
            ) for m in models
        ]

    def create_all_tables(self):
        """Создаёт таблицы (вызывать один раз при старте приложения)"""
        Base.metadata.create_all(bind=self.session.bind)