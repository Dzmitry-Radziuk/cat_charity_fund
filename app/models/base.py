from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app import constants
from app.core.db import Base


class AbstractBase(Base):
    """Абстрактная базовая модель с общими полями для проектов и донатов."""

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=constants.ZERO)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    close_date = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint("full_amount > 0", name="check_full_amount_positive"),
        CheckConstraint(
            "invested_amount >= 0", name="check_invested_amount_non_negative"
        ),
        CheckConstraint(
            "invested_amount <= full_amount", name="check_invested_le_full"
        ),
    )
