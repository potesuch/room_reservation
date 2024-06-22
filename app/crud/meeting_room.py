from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


class CRUDMeetingRoom(CRUDBase[
    MeetingRoom,
    MeetingRoomCreate,
    MeetingRoomUpdate
]):
    """
    Класс для операций CRUD с моделью MeetingRoom.
    """

    async def get_room_id_by_name(
            self,
            room_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        """
        Получает идентификатор комнаты по ее названию.

        Args:
            room_name (str): Название комнаты.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            Optional[int]: Идентификатор найденной комнаты или None, если комната не найдена.
        """
        db_room_id = await session.scalar(
            select(MeetingRoom.id).where(MeetingRoom.name == room_name)
        )
        return db_room_id


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
