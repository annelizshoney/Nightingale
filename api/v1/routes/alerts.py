from fastapi import APIRouter, Depends

from app.adk.emergency_agent import EmergencyAgent
from app.core.dependencies import get_emergency_agent
from app.schemas.agent import AgentResponse

router = APIRouter(tags=["Alerts"])


@router.get("/alerts", response_model=AgentResponse)
def alerts(agent: EmergencyAgent = Depends(get_emergency_agent)) -> AgentResponse:
    return agent.generate(
        {
            "request": "Summarize current safety alerts and escalation status.",
            "metadata": {"source": "alerts"},
        }
    )