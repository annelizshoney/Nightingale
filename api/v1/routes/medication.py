from fastapi import APIRouter, Depends

from app.adk.medication_agent import MedicationAgent
from app.core.dependencies import get_medication_agent
from app.schemas.agent import AgentResponse

router = APIRouter(tags=["Medication"])


@router.get("/medications", response_model=AgentResponse)
def medications(agent: MedicationAgent = Depends(get_medication_agent)) -> AgentResponse:
    return agent.generate(
        {
            "request": "Summarize medication adherence and next doses.",
            "metadata": {"source": "medications"},
        }
    )