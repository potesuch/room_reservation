import datetime as dt
from typing import Sequence, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate
from app.models import User


class CRUDReservation(CRUDBase[
    Reservation,
    ReservationCreate,
    ReservationUpdate
]):
    """
    Класс для операций CRUD с моделью Reservation.
    """

    async def get_reservations_at_the_same_time(
            self,
            *,
            from_reserve: dt.datetime,
            to_reserve: dt.datetime,
            meetingroom_id: int,
            reservation_id: Optional[int] = None,
            session:  AsyncSession
    ) -> Sequence[Reservation]:
        """
        Получает бронирования, происходящие в указанный период времени.

        Args:
            from_reserve (dt.datetime): Время начала бронирования.
            to_reserve (dt.datetime): Время окончания бронирования.
            meetingroom_id (int): Идентификатор переговорной комнаты.
            reservation_id (Optional[int], optional): Идентификатор бронирования (для исключения при поиске).
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            Sequence[Reservation]: Список бронирований, происходящих в указанный период.
        """
        stmt = select(Reservation).where(
            and_(
                Reservation.meetingroom_id == meetingroom_id,
                Reservation.from_reserve <= to_reserve,
                Reservation.to_reserve >= from_reserve
            )
        )
        if reservation_id is not None:
            stmt = select(Reservation).where(
                and_(
                    Reservation.id == reservation_id,
                    Reservation.from_reserve <= to_reserve,
                    Reservation.to_reserve >= from_reserve
                )
            )
        reservations = await session.scalars(stmt)
        return reservations.all()

    async def get_future_reservations_for_room(
        self,
        meetingroom_id: int,
        session: AsyncSession
    ) -> Sequence[Reservation]:
        """
        Получает будущие бронирования для комнаты.

        Args:
            meetingroom_id (int): Идентификатор переговорной комнаты.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            Sequence[Reservation]: Список будущих бронирований для указанной комнаты.
        """
        reservations = await session.scalars(select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            Reservation.to_reserve > dt.datetime.now()
        ))
        return reservations.all()

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ) -> Sequence[Reservation]:
        """
        Получает бронирования, сделанные пользователем.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            user (User): Пользователь, чьи бронирования необходимо получить.

        Returns:
            Sequence[Reservation]: Список бронирований, сделанных указанным пользователем.
        """
        reservations = await session.scalars(
            select(Reservation).where(Reservation.user_id == user.id)
        )
        return reservations.all()


reservation_crud = CRUDReservation(Reservation)
