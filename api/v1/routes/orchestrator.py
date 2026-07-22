from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_audit_service, get_lyzr_orchestrator
from app.core.context import get_request_id
from app.lyzr.orchestrator import LyzrOrchestrator
from app.schemas.orchestrator import OrchestratorRequest, OrchestratorResponse
from app.services.audit_service import AuditService

router = APIRouter(tags=["Orchestrator"])


@router.post(
    "/orchestrate",
    response_model=OrchestratorResponse,
    status_code=status.HTTP_200_OK,
)
def orchestrate(
    payload: OrchestratorRequest,
    orchestrator: LyzrOrchestrator = Depends(get_lyzr_orchestrator),
    audit_service: AuditService = Depends(get_audit_service),
) -> OrchestratorResponse:
    response = orchestrator.generate(
        request=payload.request,
        metadata=payload.metadata,
        include_support_steps=payload.include_support_steps,
    )
    audit_service.record(
        route="/api/v1/orchestrate",
        request_payload=payload.model_dump(mode="json"),
        response_payload=response,
        status=response.get("status", "success"),
        notes=get_request_id(),
    )
    return OrchestratorResponse(**response)
