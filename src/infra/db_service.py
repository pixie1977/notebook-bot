import uuid
from datetime import datetime
from typing import List

from src.core.models import User, Message
from src.infra.database import get_db_session
from src.infra.db_message_repositories import SqlAlchemyMessageRepository
from src.infra.db_user_repositories import SqlAlchemyUserRepository


def save_user(tg_id: str, age: int, name: str) -> User:
    with get_db_session() as session:
        repo = SqlAlchemyUserRepository(session=session)
        user = repo.get(tg_id)

        if user is None:
            user = User(tg_id=tg_id, age=age, name=name)
        else:
            user.age = age
            user.name = name

        repo.add(user)
        session.commit()
        saved_user = repo.get(user.tg_id)
        return saved_user
        # Если всё ок — коммит
        # Если ошибка — rollback


def save_message(tg_id: str, text: str) -> Message:
    with get_db_session() as session:
        repo = SqlAlchemyMessageRepository(session=session)
        message = Message(text=text, tg_id=tg_id, created_at=datetime.now())
        repo.add(message)
        session.commit()
        return message

def get_last_messages_by_user_tg_id(tg_id: str, count: int = 5) -> list[Message]:
        with get_db_session() as session:
            repo = SqlAlchemyMessageRepository(session=session)
            messages = repo.list_by_user_tg_id(tg_id, count)
            return messages