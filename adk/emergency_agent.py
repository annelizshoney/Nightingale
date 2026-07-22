from app.adk.base_agent import BaseAgent


class EmergencyAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="emergency_agent", prompt_name="emergency", **kwargs)
