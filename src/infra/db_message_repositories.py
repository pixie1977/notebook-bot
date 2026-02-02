from __future__ import annotations

from typing import Optional, List

from sqlalchemy.orm import Session

from .db_models import Base, MessageDbModel
from ..core.models import Message
from ..core.repositories import MessageRepository


class InMemoryMessageRepository(MessageRepository):
    def __init__(self) -> None:
        self._items: dict[str, Message] = {}

    def get(self, msg_id: str) -> Optional[MessageRepository]:
        return self._items.get(msg_id)

    def add(self, msg: Message) -> None:
        self._items[msg.uid] = msg

    def list_by_user_tg_id(self, tg_id: str, count: int) -> List[Message]:
        return [msg for msg in self._items.values() if msg.tg_id == tg_id]


class SqlAlchemyMessageRepository(MessageRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, msg_id: str) -> Optional[Message]:
        model = self.session.query(MessageDbModel).filter_by(uid=msg_id).first()
        if model:
            return Message(
                uid=model.uid,
                tg_id=model.tg_id,
                text=model.text,
                created_at=model.created_at,
            )
        return None

    def add(self, message: Message) -> None:
        model = MessageDbModel(
            tg_id=message.tg_id,
            text=message.text,
            created_at=message.created_at,
        )
        self.session.add(model)

    def list_by_user_tg_id(self, tg_id: str, count: int = 5) -> List[Message]:
        models = (
            self.session.query(MessageDbModel)
            .filter(MessageDbModel.tg_id == tg_id)
            .order_by(MessageDbModel.created_at.desc())  # сортировка по времени (новые первыми)
            .limit(count)  # берём только count последних
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

    def create_all_tables(self):
        """Создаёт таблицы (вызывать один раз при старте приложения)"""
        Base.metadata.create_all(bind=self.session.bind)