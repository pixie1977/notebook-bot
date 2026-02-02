from datetime import datetime


class User:
    """
    Описание пользователя
    Entity:
    - имеет устойчивую идентичность: uid
    - содержит состояние: uid, tg_id, name, city
    """

    def __init__(
            self,
            tg_id: str,
            name: str,
            age: int,
            uid: int = 0,
    ):
        self.uid = uid
        self.tg_id = tg_id
        self.name = name
        self.age = age


class Message:
    """
    Описание сообщения
    Entity:
    - имеет устойчивую идентичность: uid
    - содержит состояние: uid, user_id, text, created_at
    """

    def __init__(
            self,
            tg_id: str,
            text: str,
            created_at: datetime,
            uid: int = 0,
    ):
        self.uid = uid
        self.tg_id = tg_id
        self.text = text
        self.created_at = created_at
