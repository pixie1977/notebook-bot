from __future__ import annotations

from datetime import datetime
from typing import Protocol, Optional, List

from src.core.models import User, Message
from src.infra.db_models import UserDbModel


# Repository Port (выходной порт для User)
class UserRepository(Protocol):
    def get(self, user_id: str) -> Optional[User]: ...
    def add(self, user: User) -> None: ...
    def list_by_id(self, tg_id: str) -> List[User]: ...

# Repository Port (выходной порт для Message)
class MessageRepository(Protocol):
    def get(self, msg_id: str) -> Optional[Message]: ...
    def add(self, message: Message) -> None: ...
    def list_by_user_tg_id(self, tg_id: str, count: int) -> List[Message]: ...
