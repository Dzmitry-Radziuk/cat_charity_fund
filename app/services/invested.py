from datetime import datetime, timezone
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import constants
from app.models import CharityProject, Donation


async def close_if_fully_invested(obj: object, session: AsyncSession) -> None:
    """Закрывает объект, если полностью инвестирован."""
    if getattr(obj, "invested_amount", constants.ZERO) >= getattr(
        obj, "full_amount", constants.ZERO
    ) and not getattr(obj, "fully_invested", False):
        obj.fully_invested = True
        obj.close_date = datetime.now(timezone.utc)
        session.add(obj)


async def get_open_projects(session: AsyncSession) -> List[CharityProject]:
    """Возвращает список открытых проектов."""
    result = await session.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested.is_(False))
        .order_by(CharityProject.create_date)
    )
    return result.scalars().all()


async def get_open_donations(session: AsyncSession) -> List[Donation]:
    """Возвращает список открытых пожертвований."""
    result = await session.execute(
        select(Donation)
        .where(Donation.invested_amount < Donation.full_amount)
        .order_by(Donation.create_date)
    )
    return result.scalars().all()


async def distribute_funds(
    projects: List[CharityProject],
    donations: List[Donation],
    session: AsyncSession,
) -> None:
    """Распределяет средства между проектами и пожертвованиями."""
    for project in projects:
        needed = project.full_amount - project.invested_amount
        if needed <= constants.ZERO:
            continue

        for donation in donations:
            available = donation.full_amount - donation.invested_amount
            if available <= constants.ZERO:
                continue

            invest_amount = min(needed, available)
            project.invested_amount += invest_amount
            donation.invested_amount += invest_amount
            needed -= invest_amount

            if donation.invested_amount == donation.full_amount:
                await close_if_fully_invested(donation, session)

            if project.invested_amount == project.full_amount:
                await close_if_fully_invested(project, session)
                break

        if needed > constants.ZERO:
            continue


async def invest_funds(session: AsyncSession) -> List[CharityProject]:
    """Инвестирует средства из пожертвований в проекты."""
    projects = await get_open_projects(session)
    donations = await get_open_donations(session)

    if not projects or not donations:
        return projects

    await distribute_funds(projects, donations, session)
    await session.commit()

    for project in projects:
        await session.refresh(project)
    for donation in donations:
        await session.refresh(donation)

    return projects
