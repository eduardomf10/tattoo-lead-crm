"""Lead schemas."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LeadStatus(str, Enum):
    NEW = "new"
    AWAITING_CLIENT_REPLY = "awaiting_client_reply"
    IN_CONVERSATION = "in_conversation"
    SCHEDULED = "scheduled"
    CLOSED = "closed"
    LOST = "lost"


class LeadBase(BaseModel):
    client_id: int
    original_message: str | None = None
    tattoo_idea: str | None = None
    body_location: str | None = None
    size: str | None = None
    style: str | None = None
    color_type: str | None = None
    design_type: str | None = None
    summary: str | None = None
    status: LeadStatus = LeadStatus.NEW
    source: str | None = None
    estimated_budget_range: str | None = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    original_message: str | None = None
    tattoo_idea: str | None = None
    body_location: str | None = None
    size: str | None = None
    style: str | None = None
    color_type: str | None = None
    design_type: str | None = None
    summary: str | None = None
    source: str | None = None
    estimated_budget_range: str | None = None


class LeadStatusUpdate(BaseModel):
    status: LeadStatus


class LeadResponse(LeadBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class LeadDetailResponse(LeadResponse):
    """Lead with nested client (for GET /leads/{id})."""

    client: Optional["ClientResponse"] = None


# Resolve forward reference after both schemas are defined (no circular import: client doesn't import lead)
from app.schemas.client import ClientResponse  # noqa: E402
LeadDetailResponse.model_rebuild()
