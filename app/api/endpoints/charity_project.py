from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_name_duplicate,
    forbid_delete_invested_project,
    forbid_update_closed_project,
    validate_full_amount_not_less_than_invested,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.invested import (
    close_if_fully_invested,
    get_open_donations,
    invest_funds,
)


router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Создать новый проект (только для суперпользователей)."""
    await check_name_duplicate(charity_project.name, session)

    new_project = await charity_project_crud.create(
        charity_project, session, commit=False
    )

    open_donations = await get_open_donations(session)
    if open_donations:
        invest_funds(new_project, open_donations)
        session.add_all(open_donations + [new_project])
    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    update_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Обновить данные проекта (только для суперпользователей)."""
    db_project = await check_charity_project_exists(project_id, session)
    await forbid_update_closed_project(db_project)

    if update_data.name is not None and update_data.name != db_project.name:
        await check_name_duplicate(update_data.name, session)

    await validate_full_amount_not_less_than_invested(
        update_data.full_amount, db_project, session
    )

    updated_project = await charity_project_crud.update(
        db_project, update_data, session, commit=False
    )

    close_if_fully_invested(updated_project)

    open_donations = await donation_crud.get_not_fully_invested(session)

    if open_donations:
        changed_donations = invest_funds(updated_project, open_donations)
        session.add_all([updated_project] + changed_donations)
    await session.commit()
    await session.refresh(updated_project)

    return updated_project


@router.get(
    "/",
    response_model=List[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDB]:
    """Получить список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.delete(
    "/{project_id}",
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Удалить проект (только для суперпользователей)."""
    db_project = await check_charity_project_exists(project_id, session)
    await forbid_delete_invested_project(db_project)
    await forbid_update_closed_project(db_project)
    return await charity_project_crud.remove(db_project, session)
