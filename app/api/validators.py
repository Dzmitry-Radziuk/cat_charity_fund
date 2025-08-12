from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import constants
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession,
) -> None:
    """Проверить уникальность названия благотворительного проекта."""
    charity_project_id: Optional[int] = (
        await charity_project_crud.get_project_id_by_name(
            charity_project_name, session
        )
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверить существование благотворительного проекта по ID."""
    charity_project: Optional[CharityProject] = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден!"
        )
    return charity_project


async def validate_full_amount_not_less_than_invested(
    full_amount: Optional[int], project: CharityProject, session: AsyncSession
) -> CharityProject:
    """Проверить, что требуемая сумма не меньше уже вложенной."""
    if full_amount is not None and full_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Нельзя установить значение full_amount "
                "меньше уже вложенной суммы."
            ),
        )
    return project


async def forbid_update_closed_project(
    project: CharityProject,
) -> CharityProject:
    """Запретить изменение закрытого проекта."""
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект закрыт и не может быть изменён.",
        )
    return project


async def forbid_delete_invested_project(project: CharityProject) -> None:
    """Запретить удаление проекта с уже вложенными средствами."""
    if project.invested_amount > constants.ZERO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить проект, в который уже внесены средства.",
        )
