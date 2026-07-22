from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AuditLogCreate(BaseModel):
    route: str
    request_payload: dict[str, Any] = Field(default_factory=dict)
    response_payload: dict[str, Any] = Field(default_factory=dict)
    status: str
    notes: str | None = None


class AuditLogRead(AuditLogCreate):
    id: str
    request_id: str
    created_at: datetime
