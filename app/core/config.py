from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Конфигурация приложения."""

    app_title: str = "Бронирование переговорок"
    description: str = "Сервис для бронирования"
    database_uri: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
