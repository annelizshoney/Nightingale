from app.adk.base_agent import BaseAgent


class HealthAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="health_agent", prompt_name="health", **kwargs)
