import contextlib

from fastapi import FastAPI

from app.core.config import settings
from app.api.routers import main_router
from app.core.init_db import create_first_superuser


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер для жизненного цикла приложения.

    Перед стартом приложения создает первого суперпользователя.

    Parameters:
        app (FastAPI): Экземпляр FastAPI приложения.

    Yields:
        None
    """
    await create_first_superuser()
    yield


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan
)

app.include_router(main_router)
