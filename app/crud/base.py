from typing import Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс CRUD-операций."""

    def __init__(self, model: Type[ModelType]):
        """Инициализация с указанной моделью SQLAlchemy."""
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        """Получить объект по ID."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession) -> list[ModelType]:
        """Получить список всех объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in: Union[CreateSchemaType, dict],
        session: AsyncSession,
        user: Optional[User] = None,
        commit: bool = True,
    ) -> ModelType:
        """Создать новый объект, при необходимости указав владельца."""
        obj_in_data = obj_in.dict() if hasattr(obj_in, "dict") else obj_in
        if user is not None:
            obj_in_data["user_id"] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, dict],
        session: AsyncSession,
        commit: bool = True,
    ) -> ModelType:
        """Обновить объект по переданным данным."""
        obj_data = jsonable_encoder(db_obj)
        update_data = (
            obj_in.dict(exclude_unset=True)
            if hasattr(obj_in, "dict")
            else obj_in
        )
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
        commit: bool = True,
    ) -> ModelType:
        """Удалить объект."""
        await session.delete(db_obj)
        if commit:
            await session.commit()
        return db_obj

    async def get_not_fully_invested(
        self, session: AsyncSession
    ) -> list[ModelType]:
        """Вернуть список объектов, которые ещё не полностью инвестированы."""
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return result.scalars().all()
