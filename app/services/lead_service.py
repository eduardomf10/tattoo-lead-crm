"""Lead service - business logic for leads."""

from sqlalchemy.orm import Session, joinedload

from app.models import Lead
from app.schemas.lead import LeadCreate, LeadStatus, LeadStatusUpdate


def create_lead(db: Session, data: LeadCreate) -> Lead:
    """Create a new lead."""
    lead = Lead(**data.model_dump(mode="json"))
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def get_lead(db: Session, lead_id: int, with_client: bool = False) -> Lead | None:
    """Get a lead by ID, optionally with client loaded."""
    q = db.query(Lead).filter(Lead.id == lead_id)
    if with_client:
        q = q.options(joinedload(Lead.client))
    return q.first()


def get_leads(
    db: Session,
    status: LeadStatus | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Lead]:
    """List leads with optional status filter and pagination."""
    q = db.query(Lead).order_by(Lead.updated_at.desc())
    if status is not None:
        q = q.filter(Lead.status == status.value)
    return q.offset(skip).limit(limit).all()


def update_lead_status(db: Session, lead_id: int, data: LeadStatusUpdate) -> Lead | None:
    """Update lead status."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return None
    lead.status = data.status.value
    db.commit()
    db.refresh(lead)
    return lead
