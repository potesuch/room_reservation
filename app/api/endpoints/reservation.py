from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.reservation import (ReservationDB, ReservationCreate,
                                     ReservationUpdate)
from app.api.validators import (check_reservation_intersections,
                                check_meeting_room_exists,
                                check_reservation_before_edit)
from app.crud.reservation import reservation_crud
from app.models import User
from app.core.user import current_user, current_superuser

router = APIRouter()


@router.post(
    '/',
    response_model=ReservationDB,
    response_model_exclude_none=True
)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Создает новое бронирование.
    """
    await check_meeting_room_exists(reservation.meetingroom_id, session)
    await check_reservation_intersections(
        **reservation.model_dump(), session=session
    )
    new_reservation = await reservation_crud.create(reservation, session, user)
    return new_reservation


@router.get(
    '/',
    response_model=list[ReservationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Получает список всех бронирований.
    """
    reservations = await reservation_crud.get_multi(session)
    return reservations


@router.delete(
    '/{reservation_id}',
    response_model=ReservationDB,
    response_model_exclude_none=True
)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Для суперюзеров или создателей объекта бронирования.

    Удаляет бронирование по его идентификатору.
    """
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    reservation = await reservation_crud.remove(reservation, session)
    return reservation


@router.patch(
    '/{reservation_id}',
    response_model=ReservationDB,
    response_model_exclude_none=True
)
async def update_reservation(
    reservation_id: int,
    reservation_in: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Для суперюзеров или создателей объекта бронирования."""
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    await check_reservation_intersections(
        **reservation_in.model_dump(),
        reservation_id=reservation_id,
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        reservation, reservation_in, session
    )
    return reservation


@router.get(
    '/my_reservations',
    response_model=list[ReservationDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'}
)
async def get_my_reservations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Получает список всех бронирований для текущего пользователя.
    """
    reservations = await reservation_crud.get_by_user(session, user)
    return reservations
