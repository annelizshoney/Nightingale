from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.adk.client import ADKClient
from app.core.context import get_request_id
from app.lyzr.client import LyzrClient
from app.qdrant.client import QdrantMemoryClient


class HealthService:
	def __init__(
		self,
		*,
		qdrant_client: QdrantMemoryClient,
		adk_client: ADKClient,
		lyzr_client: LyzrClient,
	) -> None:
		self.qdrant_client = qdrant_client
		self.adk_client = adk_client
		self.lyzr_client = lyzr_client

	def check_database(self, db: Session) -> dict[str, Any]:
		db.execute(text("SELECT 1"))
		return {"status": "ready"}

	def check_qdrant(self) -> dict[str, Any]:
		return self.qdrant_client.health_check()

	def check_adk(self) -> dict[str, Any]:
		return self.adk_client.health_check()

	def check_lyzr(self) -> dict[str, Any]:
		return self.lyzr_client.health_check()

	def build_report(self, db: Session) -> dict[str, Any]:
		checks = [
			{"component": "database", **self.check_database(db)},
			{"component": "qdrant", **self.check_qdrant()},
			{"component": "google_adk", **self.check_adk()},
			{"component": "lyzr", **self.check_lyzr()},
		]
		overall = "healthy" if all(check["status"] == "ready" for check in checks) else "degraded"
		return {
			"status": overall,
			"request_id": get_request_id(),
			"checks": checks,
			"metadata": {},
		}

