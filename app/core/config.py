from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения.
    
    Attributes:
        app_title (str): Название приложения.
        app_description (str): Описание приложения.
        database_url (str): URL базы данных.
        secret (str): Секретный ключ приложения.
        first_superuser_email (Optional[EmailStr]): Email первого суперпользователя.
        first_superuser_password (Optional[str]): Пароль первого суперпользователя.
        model_config (SettingsConfigDict): Конфигурация модели.
    """
    app_title: str = 'Title'
    app_description: str = 'Description'
    database_url: str = 'sqlite:///sqlite.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8')


settings = Settings()
