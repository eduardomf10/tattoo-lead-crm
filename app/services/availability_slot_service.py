"""AvailabilitySlot service - business logic for availability slots."""

from sqlalchemy.orm import Session

from app.models import AvailabilitySlot
from app.schemas.availability_slot import AvailabilitySlotCreate


def create_slot(db: Session, data: AvailabilitySlotCreate) -> AvailabilitySlot:
    slot = AvailabilitySlot(**data.model_dump())
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot


def list_available_slots(db: Session) -> list[AvailabilitySlot]:
    return db.query(AvailabilitySlot).filter(AvailabilitySlot.is_booked.is_(False)).all()


def get_slot(db: Session, slot_id: int) -> AvailabilitySlot | None:
    return db.query(AvailabilitySlot).filter(AvailabilitySlot.id == slot_id).first()

