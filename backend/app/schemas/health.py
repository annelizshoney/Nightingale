from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HealthCheckDetail(BaseModel):
    component: str
    status: str
    details: dict[str, Any] = Field(default_factory=dict)


class HealthCheckResponse(BaseModel):
    status: str
    request_id: str
    checks: list[HealthCheckDetail] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
