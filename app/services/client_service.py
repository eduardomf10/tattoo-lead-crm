"""Client service - business logic for clients."""

from sqlalchemy.orm import Session

from app.models import Client
from app.schemas.client import ClientCreate


def create_client(db: Session, data: ClientCreate) -> Client:
    """Create a new client."""
    client = Client(**data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def get_client(db: Session, client_id: int) -> Client | None:
    """Get a client by ID."""
    return db.query(Client).filter(Client.id == client_id).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100) -> list[Client]:
    """List clients with optional pagination."""
    return db.query(Client).order_by(Client.created_at.desc()).offset(skip).limit(limit).all()
