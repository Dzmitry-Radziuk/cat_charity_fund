from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt

from app import constants


class BaseProjectAndDonationDB(BaseModel):
    """Базовая схема с общими полями для проектов и пожертвований."""

    id: PositiveInt
    invested_amount: NonNegativeInt
    fully_invested: bool = False
    full_amount: PositiveInt
    create_date: datetime
    close_date: Optional[datetime] = None


class CharityProjectBase(BaseModel):
    """Базовая схема для обновления и создания проекта."""

    name: Optional[str] = Field(
        None, min_length=constants.ONE, max_length=constants.ONE_HUNDRED
    )
    description: Optional[str] = Field(
        None, min_length=constants.ONE, max_length=constants.FIVE_HUNDRED
    )
    full_amount: Optional[PositiveInt]

    class Config:
        extra = "forbid"


class DonationBase(BaseModel):
    """Базовая схема для пожертвования."""

    comment: Optional[str] = None
