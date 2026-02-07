"""
Модуль инициализации базы данных.
Содержит настройку движка, сессии и контекстного менеджера для работы с SQLAlchemy.
"""
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config.config import DB_ADDR
from src.infra.db_models import Base


# Создание движка БД (используем SQLite для простоты; в продакшене — конфигурировать)
engine = create_engine(DB_ADDR, echo=True)

# Фабрика сессий
SessionLocal = sessionmaker(bind=engine)


@contextmanager
def get_db_session() -> Session:
    """
    Контекстный менеджер для получения сессии SQLAlchemy.
    Автоматически фиксирует транзакцию при успехе, откатывает при ошибке.

    :yield: объект сессии.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# Создание таблиц при импорте модуля (выполняется один раз)
with get_db_session() as session:
    Base.metadata.create_all(bind=session.bind)