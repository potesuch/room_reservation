from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import (DeclarativeBase, declared_attr, Mapped,
                            mapped_column)

from app.core.config import settings


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей.

    Attributes:
        __tablename__ (str): Имя таблицы, устанавливается как имя класса в нижнем регистре.
        id (Mapped[int]): Первичный ключ.
    """

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


engine = create_async_engine(settings.database_url, echo=True)

async_session = async_sessionmaker(engine)


async def get_async_session():
    """
    Создает асинхронную сессию для работы с базой данных.

    Returns:
        AsyncSession: Асинхронная сессия SQLAlchemy.
    """
    async with async_session() as session:
        yield session
