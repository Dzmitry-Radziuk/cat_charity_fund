from sqlalchemy import CheckConstraint, Column, String, Text

from app import constants
from app.models.base import AbstractBase


class CharityProject(AbstractBase):
    """Модель благотворительного проекта."""

    __tablename__ = "charityproject"

    name = Column(String(constants.ONE_HUNDRED), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint("length(name) >= 1", name="name_min_length"),
        CheckConstraint(
            "length(description) >= 1", name="description_min_length"
        ),
    )
