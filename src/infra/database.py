from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional, Any, Generator

from src.infra.db_models import Base

# TODO:: Движок БД (используем SQLite для простоты, в проме вынести в конфиг)
engine = create_engine("sqlite:///tg_data.db", echo=True)

# Фабрика сессий
SessionLocal = sessionmaker(bind=engine)


# Зависимость для получения сессии (полезно при интеграции с FastAPI и т.п.)
@contextmanager
def get_db_session() -> Session:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


with get_db_session() as session:
    Base.metadata.create_all(bind=session.bind)
