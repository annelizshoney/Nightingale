from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, audit_log: AuditLog) -> AuditLog:
        self.session.add(audit_log)
        self.session.commit()
        self.session.refresh(audit_log)
        return audit_log
