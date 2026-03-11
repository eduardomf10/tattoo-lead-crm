"""Lead model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    original_message = Column(Text, nullable=True)
    tattoo_idea = Column(Text, nullable=True)
    body_location = Column(String(255), nullable=True)
    size = Column(String(100), nullable=True)
    style = Column(String(100), nullable=True)
    color_type = Column(String(50), nullable=True)  # e.g. black_and_grey, color
    design_type = Column(String(100), nullable=True)
    summary = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="new")
    source = Column(String(100), nullable=True)  # e.g. instagram_dm, email, referral
    estimated_budget_range = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("Client", back_populates="leads")
    notes = relationship("Note", back_populates="lead", cascade="all, delete-orphan")
    appointment = relationship(
        "Appointment",
        back_populates="lead",
        uselist=False,
        cascade="all, delete-orphan",
    )
