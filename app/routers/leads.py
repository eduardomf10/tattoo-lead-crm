"""Lead routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.lead import (
    LeadCreate,
    LeadDetailResponse,
    LeadResponse,
    LeadStatus,
    LeadStatusUpdate,
)
from app.services import lead_service

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("", response_model=LeadResponse)
def create_lead(data: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead."""
    return lead_service.create_lead(db, data)


@router.get("", response_model=list[LeadResponse])
def list_leads(
    status: LeadStatus | None = Query(None, description="Filter by lead status"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List leads, optionally filtered by status."""
    return lead_service.get_leads(db, status=status, skip=skip, limit=limit)


@router.get("/{lead_id}", response_model=LeadDetailResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get a lead by ID with client details."""
    lead = lead_service.get_lead(db, lead_id, with_client=True)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.patch("/{lead_id}/status", response_model=LeadResponse)
def update_lead_status(lead_id: int, data: LeadStatusUpdate, db: Session = Depends(get_db)):
    """Update lead status."""
    lead = lead_service.update_lead_status(db, lead_id, data)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead
