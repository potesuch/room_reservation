import datetime as dt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Reservation(Base):
    """
    Модель бронирования переговорной комнаты.

    Attributes:
        from_reserve (Mapped[dt.datetime]): Время начала бронирования.
        to_reserve (Mapped[dt.datetime]): Время окончания бронирования.
        meetingroom_id (Mapped[int]): Внешний ключ на переговорную комнату.
        user_id (Mapped[int]): Внешний ключ на пользователя, сделавшего бронирование.
    """
    from_reserve: Mapped[dt.datetime]
    to_reserve: Mapped[dt.datetime]
    meetingroom_id: Mapped[int] = mapped_column(ForeignKey('meetingroom.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    def __repr__(self):
        return (
            f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
        )
