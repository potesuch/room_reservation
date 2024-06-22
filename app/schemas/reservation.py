import datetime as dt

from pydantic import (BaseModel, ConfigDict, Field, field_validator,
                      model_validator)

FROM_TIME = (
    dt.datetime.now() + dt.timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    dt.datetime.now() + dt.timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    """
    Базовая модель бронирования.

    Attributes:
        from_reserve (dt.datetime): Время начала бронирования.
        to_reserve (dt.datetime): Время окончания бронирования.
    """
    from_reserve: dt.datetime = Field(examples=[FROM_TIME])
    to_reserve: dt.datetime = Field(examples=[TO_TIME])


class ReservationUpdate(ReservationBase):
    """
    Модель для обновления бронирования.

    Inherits:
        ReservationBase: Базовая модель бронирования.

    Config:
        model_config (ConfigDict): Конфигурация модели для запрета дополнительных полей при валидации.
    """
    model_config = ConfigDict(extra='forbid')

    @field_validator('from_reserve')
    @classmethod
    def check_from_reserve_later_than_now(csl, value):
        if value <= dt.datetime.now():
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return value

    @model_validator(mode='after')
    def check_from_reserve_before_than_to_reserve(self):
        if self.from_reserve >= self.to_reserve:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return self


class ReservationCreate(ReservationUpdate):
    """
    Модель для создания нового бронирования.

    Inherits:
        ReservationUpdate: Модель для обновления бронирования.

    Attributes:
        meetingroom_id (int): Идентификатор переговорной комнаты.
    """
    meetingroom_id: int


class ReservationDB(ReservationBase):
    """
    Модель бронирования в базе данных.

    Inherits:
        ReservationBase: Базовая модель бронирования.

    Attributes:
        id (int): Идентификатор бронирования.
        meetingroom_id (int): Идентификатор переговорной комнаты.
        user_id (int): Идентификатор пользователя, создавшего бронирование.
    """
    id: int
    meetingroom_id: int
    user_id: int
