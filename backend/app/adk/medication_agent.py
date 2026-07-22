from app.adk.base_agent import BaseAgent


class MedicationAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="medication_agent", prompt_name="medication", **kwargs)
