from typing import Optional
from pydantic import BaseModel, Field, field_validator


class MeetingRoomBase(BaseModel):
    """
    Базовая модель переговорной комнаты.

    Attributes:
        name (Optional[str]): Имя переговорной комнаты.
        description (Optional[str]): Описание переговорной комнаты.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class MeetingRoomCreate(MeetingRoomBase):
    """
    Модель для создания новой переговорной комнаты.

    Attributes:
        name (str): Имя переговорной комнаты.
    """
    name: str = Field(min_length=1, max_length=100)


class MeetingRoomUpdate(MeetingRoomBase):
    """
    Модель для обновления переговорной комнаты.

    Attributes:
        name (Optional[str]): Имя переговорной комнаты.
    """

    @field_validator('name')
    @classmethod
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


class MeetingRoomDB(MeetingRoomCreate):
    """
    Модель переговорной комнаты в базе данных.

    Inherits:
        MeetingRoomCreate: Модель для создания новой переговорной комнаты.

    Attributes:
        id (int): Идентификатор переговорной комнаты.
    """
    id: int
