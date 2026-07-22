from fastapi import APIRouter, Depends

from app.adk.emergency_agent import EmergencyAgent
from app.core.dependencies import get_emergency_agent
from app.schemas.agent import AgentResponse

router = APIRouter(tags=["Emergency"])


@router.get("/emergency", response_model=AgentResponse)
def emergency(agent: EmergencyAgent = Depends(get_emergency_agent)) -> AgentResponse:
    return agent.generate(
        {
            "request": "Assess current emergency risk and escalation guidance.",
            "metadata": {"source": "emergency"},
        }
    )
