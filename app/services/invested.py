from datetime import datetime, timezone
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import constants
from app.models import CharityProject, Donation


def close_if_fully_invested(obj: Union[CharityProject, Donation]) -> None:
    """Закрывает объект, если полностью инвестирован."""
    if obj.invested_amount >= obj.full_amount and not obj.fully_invested:
        obj.fully_invested = True
        obj.close_date = datetime.now(timezone.utc)


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
        .where(Donation.fully_invested.is_(False))
        .order_by(Donation.create_date)
    )
    return result.scalars().all()


def invest_funds(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]],
) -> None:
    """Распределяет средства между новым объектом и списком открытых."""
    for source in sources:
        invest_amount: int = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount,
        )

        if invest_amount <= constants.ZERO:
            continue

        for obj in (target, source):
            obj.invested_amount += invest_amount
            close_if_fully_invested(obj)

        if target.fully_invested:
            break
