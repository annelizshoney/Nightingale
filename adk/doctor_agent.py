from app.adk.base_agent import BaseAgent


class DoctorAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="doctor_agent", prompt_name="doctor", **kwargs)
