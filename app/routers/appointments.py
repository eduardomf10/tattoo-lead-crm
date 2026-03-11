"""Appointment routes (nested under leads)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.services import appointment_service, lead_service

router = APIRouter(prefix="/leads", tags=["appointments"])


@router.post("/{lead_id}/appointment", response_model=AppointmentResponse)
def create_or_update_appointment(
    lead_id: int, data: AppointmentCreate, db: Session = Depends(get_db)
):
    """Create or update the appointment for a lead (one per lead)."""
    appointment = appointment_service.create_appointment(db, lead_id, data)
    if not appointment:
        raise HTTPException(status_code=404, detail="Lead not found")
    return appointment


@router.get("/{lead_id}/appointment", response_model=AppointmentResponse | None)
def get_appointment(lead_id: int, db: Session = Depends(get_db)):
    """Get the appointment for a lead, if any."""
    if not lead_service.get_lead(db, lead_id):
        raise HTTPException(status_code=404, detail="Lead not found")
    return appointment_service.get_appointment_by_lead(db, lead_id)
