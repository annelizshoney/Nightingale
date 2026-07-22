from fastapi import APIRouter, Depends

from app.adk.routine_agent import RoutineAgent
from app.core.dependencies import get_routine_agent
from app.schemas.agent import AgentResponse

router = APIRouter(tags=["Routine"])


@router.get("/routine", response_model=AgentResponse)
def routine(agent: RoutineAgent = Depends(get_routine_agent)) -> AgentResponse:
    return agent.generate(
        {
            "request": "Analyze routine consistency and disruptions.",
            "metadata": {"source": "routine"},
        }
    )
