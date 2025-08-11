from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class DonationCRUD(CRUDBase):
    """CRUD-операции для модели Donation."""

    async def get_by_donation(self, session: AsyncSession, user: User):
        """Получить пожертвования пользователя."""
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = DonationCRUD(Donation)
