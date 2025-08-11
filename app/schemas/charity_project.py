from pydantic import Field, PositiveInt, root_validator

from app import constants
from app.schemas.base import BaseProjectAndDonationDB, CharityProjectBase


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания проекта с обязательными полями."""

    name: str = Field(
        ..., min_length=constants.ONE, max_length=constants.ONE_HUNDRED
    )
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления проекта с проверкой на пустые строки."""

    @root_validator
    def check_no_empty_strings(cls, values):
        for field_name in ["name", "description"]:
            value = values.get(field_name)
            if value is not None and not value.strip():
                raise ValueError(f"{field_name} не может быть пустой строкой")
        return values


class CharityProjectDB(CharityProjectBase, BaseProjectAndDonationDB):
    """Схема для отображения проекта из БД."""

    class Config:
        orm_mode = True
