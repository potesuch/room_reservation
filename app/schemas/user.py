from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """
    Модель чтения данных пользователя.
    """
    pass


class UserCreate(schemas.BaseUserCreate):
    """
    Модель для создания нового пользователя.
    """
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """
    Модель для обновления данных пользователя.
    """
    pass
