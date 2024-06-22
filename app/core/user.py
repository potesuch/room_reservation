from typing import Optional, Union

from fastapi import Depends, Request

from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Получает экземпляр базы данных пользователей SQLAlchemyUserDatabase.

    Args:
        session (AsyncSession, optional): Асинхронная сессия SQLAlchemy. Defaults to Depends(get_async_session).

    Returns:
        SQLAlchemyUserDatabase: Экземпляр базы данных пользователей SQLAlchemy.
    """
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """
    Получает стратегию JWT для аутентификации.

    Returns:
        JWTStrategy: Стратегия JWT.
    """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Менеджер пользователей.

    Управляет созданием, валидацией паролей и другими операциями с пользователями.

    Attributes:
        ...

    Methods:
        validate_password(password: str, user: Union[UserCreate, User]) -> None:
            Валидирует пароль пользователя.

        on_after_register(user: User, request: Optional[Request] = None):
            Вызывается после регистрации пользователя.
    """

    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User]
    ) -> None:
        """
        Валидирует пароль пользователя.

        Args:
            password (str): Пароль для валидации.
            user (Union[UserCreate, User]): Модель пользователя или данные создания пользователя.

        Raises:
            InvalidPasswordException: Если пароль не соответствует требованиям.
        """
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain email'
            )

    # async def on_after_register(
    #         self, user: User, request: Optional[Request] = None
    # ):
    #     """
    #     Вызывается после регистрации пользователя.

    #     Args:
    #         user (User): Зарегистрированный пользователь.
    #         request (Optional[Request], optional): Запрос. Defaults to None.
    #     """
    #     print(f'Пользователь {user.email} зарегестрирован')


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Получает экземпляр менеджера пользователей.

    Args:
        user_db: База данных пользователей.

    Returns:
        UserManager: Менеджер пользователей.
    """
    yield UserManager(user_db)


fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
