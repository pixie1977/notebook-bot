"""
Модель доменной области: определяет сущности User и Message.
Служит основой для бизнес-логики, независима от внешних слоёв (БД, API).
"""
from datetime import datetime


class User:
    """
    Сущность пользователя.

    Entity:
    - имеет устойчивую идентичность (uid)
    - содержит состояние: tg_id, name, age

    :param tg_id: строковый идентификатор пользователя в Telegram.
    :param name: имя пользователя.
    :param age: возраст пользователя.
    :param uid: внутренний идентификатор (по умолчанию 0).
    """

    def __init__(
        self,
        tg_id: str,
        name: str,
        age: int,
        uid: int = 0,
    ) -> None:
        self.uid: int = uid
        self.tg_id: str = tg_id
        self.name: str = name
        self.age: int = age

    def __repr__(self) -> str:
        return f"User(uid={self.uid}, tg_id='{self.tg_id}', name='{self.name}', age={self.age})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return (
            self.tg_id == other.tg_id
            and self.name == other.name
            and self.age == other.age
            and self.uid == other.uid
        )


class Message:
    """
    Сущность сообщения.

    Entity:
    - имеет устойчивую идентичность (uid)
    - содержит состояние: tg_id, text, created_at

    :param tg_id: строковый идентификатор отправителя.
    :param text: текст сообщения.
    :param created_at: дата и время создания.
    :param uid: внутренний идентификатор (по умолчанию 0).
    """

    def __init__(
        self,
        tg_id: str,
        text: str,
        created_at: datetime,
        uid: int = 0,
    ) -> None:
        self.uid: int = uid
        self.tg_id: str = tg_id
        self.text: str = text
        self.created_at: datetime = created_at

    def __repr__(self) -> str:
        return (
            f"Message(uid={self.uid}, tg_id='{self.tg_id}', "
            f"text='{self.text}', created_at={self.created_at})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Message):
            return NotImplemented
        return (
            self.tg_id == other.tg_id
            and self.text == other.text
            and self.created_at == other.created_at
            and self.uid == other.uid
        )