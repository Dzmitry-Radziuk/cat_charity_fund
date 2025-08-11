from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.models.base import AbstractBase


class Donation(AbstractBase):
    """Модель пожертвования."""

    __tablename__ = "donation"

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="donations")
    comment = Column(Text)
