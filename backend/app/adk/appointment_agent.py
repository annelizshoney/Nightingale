from app.adk.base_agent import BaseAgent


class AppointmentAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="appointment_agent", prompt_name="appointment", **kwargs)
