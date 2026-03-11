"""Availability slot routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.availability_slot import (
    AvailabilitySlotCreate,
    AvailabilitySlotResponse,
)
from app.services import availability_slot_service


router = APIRouter(prefix="/slots", tags=["availability"])


@router.post("", response_model=AvailabilitySlotResponse)
def create_slot(data: AvailabilitySlotCreate, db: Session = Depends(get_db)):
    """Create a new availability slot for the artist."""
    return availability_slot_service.create_slot(db, data)


@router.get("/available", response_model=list[AvailabilitySlotResponse])
def list_available_slots(db: Session = Depends(get_db)):
    """List all slots that are not yet booked."""
    return availability_slot_service.list_available_slots(db)

