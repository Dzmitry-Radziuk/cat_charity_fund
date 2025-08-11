from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationRetrieve
from app.services.invested import invest_funds


router = APIRouter()


@router.post(
    "/",
    response_model=DonationRetrieve,
    dependencies=[Depends(current_user)],
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создать новое пожертвование (для авторизованных пользователей)."""
    new_donation = await donation_crud.create(donation, session, user)
    open_projects = await charity_project_crud.has_not_fully_invested(session)
    if open_projects:
        await invest_funds(session)
        await session.refresh(new_donation)
    return new_donation


@router.get(
    "/my",
    dependencies=[Depends(current_user)],
    response_model=list[DonationRetrieve],
    response_model_exclude_none=True,
)
async def get_by_user_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получить список пожертвований текущего пользователя."""
    return await donation_crud.get_by_donation(session, user)


@router.get(
    "/",
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Получить список всех пожертвований (только для суперпользователей)."""
    return await donation_crud.get_multi(session)
