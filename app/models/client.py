"""Client model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    instagram_handle = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    preferred_contact_method = Column(String(50), nullable=True)  # e.g. instagram, phone, email
    created_at = Column(DateTime, default=datetime.utcnow)

    leads = relationship("Lead", back_populates="client", cascade="all, delete-orphan")
