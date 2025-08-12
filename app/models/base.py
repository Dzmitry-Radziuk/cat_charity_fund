from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app import constants
from app.core.db import Base


class AbstractBase(Base):
    """Абстрактная базовая модель с общими полями для проектов и донатов."""

    __abstract__ = True

    full_amount: int = Column(Integer, nullable=False)
    invested_amount: int = Column(
        Integer, nullable=False, default=constants.ZERO
    )
    fully_invested: bool = Column(Boolean, default=False, nullable=False)
    create_date: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    close_date: Optional[datetime] = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint("full_amount > 0", name="check_full_amount_positive"),
        CheckConstraint(
            "invested_amount >= 0", name="check_invested_amount_non_negative"
        ),
        CheckConstraint(
            "invested_amount <= full_amount", name="check_invested_le_full"
        ),
    )

    def __init__(self, **kwargs: Any) -> None:
        if "invested_amount" not in kwargs:
            kwargs["invested_amount"] = constants.ZERO
        super().__init__(**kwargs)
