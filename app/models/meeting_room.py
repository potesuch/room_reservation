from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.reservation import Reservation


class MeetingRoom(Base):
    """
    Модель переговорной комнаты.

    Attributes:
        __tablename__ (str): Имя таблицы, устанавливается как имя класса в нижнем регистре.
        id (Mapped[int]): Первичный ключ.
        name (Mapped[str]): Название переговорной комнаты.
        description (Mapped[Optional[str]]): Описание переговорной комнаты.
        location (Mapped[str]): Местоположение переговорной комнаты.
        reservations (relationship): Связь с моделью бронирований.
    """
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    reservations: Mapped[list['Reservation']] = relationship(cascade='delete')
