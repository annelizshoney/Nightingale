from fastapi import APIRouter, Depends

from app.adk.appointment_agent import AppointmentAgent
from app.core.dependencies import get_appointment_agent
from app.schemas.agent import AgentResponse

router = APIRouter(tags=["Appointment"])


@router.get("/appointment", response_model=AgentResponse)
def appointment(agent: AppointmentAgent = Depends(get_appointment_agent)) -> AgentResponse:
    return agent.generate(
        {
            "request": "Summarize appointment scheduling needs and upcoming visits.",
            "metadata": {"source": "appointment"},
        }
    )
