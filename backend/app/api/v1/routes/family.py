from fastapi import APIRouter, Depends

from app.adk.family_agent import FamilyAgent
from app.core.dependencies import get_family_agent
from app.schemas.agent import AgentResponse

router = APIRouter(tags=["Family"])


@router.get("/family", response_model=AgentResponse)
def family(agent: FamilyAgent = Depends(get_family_agent)) -> AgentResponse:
    return agent.generate(
        {
            "request": "Summarize family coordination and notification status.",
            "metadata": {"source": "family"},
        }
    )