from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Модели User (id, tg_id, name, city) и Message(id, user_id, text, created_at).

class UserDbModel(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    tg_id: Column = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    modification_time = Column(DateTime, nullable=False)


class MessageDbModel(Base):
    __tablename__ = "messages"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
