"""AvailabilitySlot model."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class AvailabilitySlot(Base):
    __tablename__ = "availability_slots"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    appointment = relationship(
        "Appointment",
        back_populates="slot",
        uselist=False,
        cascade="all, delete-orphan",
    )

