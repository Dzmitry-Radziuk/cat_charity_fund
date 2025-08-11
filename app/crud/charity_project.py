from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CharityProjectCRUD(CRUDBase):
    """CRUD-операции для модели CharityProject."""

    async def get_project_id_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получить ID проекта по его имени."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        return db_project_id.scalars().first()


charity_project_crud = CharityProjectCRUD(CharityProject)
