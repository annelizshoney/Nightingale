from fastapi import APIRouter, Depends

from app.core.dependencies import get_health_service
from app.schemas.health import HealthCheckResponse
from app.services.health_service import HealthService
from app.db.session import get_db

router = APIRouter(tags=["Health"])


@router.get("/health")
def health(db=Depends(get_db), service: HealthService = Depends(get_health_service)) -> HealthCheckResponse:
    return HealthCheckResponse(**service.build_report(db))