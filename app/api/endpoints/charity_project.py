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
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.invested import close_if_fully_invested, invest_funds


router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создать новый проект (только для суперпользователей)."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    open_projects = await charity_project_crud.has_not_fully_invested(session)
    if open_projects:
        await invest_funds(session)
        await session.refresh(new_project)
    return new_project


@router.get(
    "/",
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получить список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    update_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновить данные проекта (только для суперпользователей)."""
    db_project = await check_charity_project_exists(project_id, session)
    await forbid_update_closed_project(db_project)
    if update_data.name is not None and update_data.name != db_project.name:
        await check_name_duplicate(update_data.name, session)
    await validate_full_amount_not_less_than_invested(
        update_data.full_amount, db_project, session
    )
    updated_project = await charity_project_crud.update(
        db_project, update_data, session
    )
    await close_if_fully_invested(updated_project, session)
    open_projects = await charity_project_crud.has_not_fully_invested(session)
    if open_projects:
        await invest_funds(session)
        await session.refresh(updated_project)
    return updated_project


@router.delete(
    "/{project_id}",
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
)
async def delete(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Удалить проект (только для суперпользователей)."""
    db_project = await check_charity_project_exists(project_id, session)
    await forbid_delete_invested_project(db_project)
    await forbid_update_closed_project(db_project)
    return await charity_project_crud.remove(db_project, session)
