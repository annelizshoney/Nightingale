from fastapi import APIRouter, Depends

from app.adk.doctor_agent import DoctorAgent
from app.core.dependencies import get_doctor_agent
from app.schemas.agent import AgentResponse

router = APIRouter(tags=["Doctor"])


@router.get("/doctor-summary", response_model=AgentResponse)
def doctor_summary(agent: DoctorAgent = Depends(get_doctor_agent)) -> AgentResponse:
    return agent.generate(
        {
            "request": "Prepare a concise clinical summary for the doctor.",
            "metadata": {"source": "doctor_summary"},
        }
    )