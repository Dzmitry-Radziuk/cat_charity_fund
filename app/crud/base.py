from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """Базовый класс CRUD-операций."""

    def __init__(self, model):
        """Инициализация с указанной моделью SQLAlchemy."""
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        """Получить объект по ID."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        """Получить список всех объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self, obj_in, session: AsyncSession, user: Optional[User] = None
    ):
        """Создать новый объект, при необходимости указав владельца."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["user_id"] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        """Обновить объект по переданным данным."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        """Удалить объект."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def has_not_fully_invested(self, session: AsyncSession) -> bool:
        """Проверить, есть ли незавершённые инвестиции."""
        query = select(exists().where(self.model.fully_invested.is_(False)))
        result = await session.execute(query)
        return result.scalar()
