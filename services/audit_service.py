from __future__ import annotations

from typing import Any

from app.core.context import get_request_id
from app.models.audit_log import AuditLog
from app.repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self, repository: AuditRepository) -> None:
        self.repository = repository

    def record(
        self,
        *,
        route: str,
        request_payload: dict[str, Any],
        response_payload: dict[str, Any],
        status: str,
        notes: str | None = None,
    ) -> AuditLog:
        return self.repository.create(
            AuditLog(
                request_id=get_request_id(),
                route=route,
                request_payload=request_payload,
                response_payload=response_payload,
                status=status,
                notes=notes,
            )
        )
