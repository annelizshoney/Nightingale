from fastapi import APIRouter, Depends

from app.core.dependencies import get_lyzr_orchestrator
from app.lyzr.orchestrator import LyzrOrchestrator
from app.schemas.agent import AgentResponse

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard", response_model=AgentResponse)
def dashboard(orchestrator: LyzrOrchestrator = Depends(get_lyzr_orchestrator)) -> AgentResponse:
    return orchestrator.generate(
        request="Generate the current Nightingale dashboard summary.",
        metadata={"source": "dashboard"},
    )