from datetime import datetime

from pydantic import PositiveInt

from app.schemas.base import BaseProjectAndDonationDB, DonationBase


class DonationCreate(DonationBase):
    """Схема создания пожертвования с обязательным full_amount."""

    full_amount: PositiveInt


class DonationRetrieve(DonationCreate):
    """Схема получения пожертвования с id и датой создания."""

    id: PositiveInt
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationBase, BaseProjectAndDonationDB):
    """Схема пожертвования из БД с user_id."""

    user_id: int

    class Config:
        orm_mode = True
