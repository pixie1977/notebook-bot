"""
ORM-модели для работы с базой данных.
Связывает доменные сущности с таблицами в БД через SQLAlchemy.
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UserDbModel(Base):
    """
    ORM-модель пользователя.
    Соответствует таблице 'users' в базе данных.
    """
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String(32), nullable=False, index=True)
    name = Column(String(64), nullable=False)
    age = Column(Integer, nullable=False)
    modification_time = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self) -> str:
        return (
            f"UserDbModel(uid={self.uid}, tg_id='{self.tg_id}', "
            f"name='{self.name}', age={self.age}, modification_time={self.modification_time})"
        )


class MessageDbModel(Base):
    """
    ORM-модель сообщения.
    Соответствует таблице 'messages' в базе данных.
    """
    __tablename__ = "messages"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String(32), nullable=False, index=True)
    text = Column(String(2048), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self) -> str:
        return (
            f"MessageDbModel(uid={self.uid}, tg_id='{self.tg_id}', "
            f"text='{self.text}', created_at={self.created_at})"
        )