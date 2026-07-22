from app.adk.base_agent import BaseAgent


class FamilyAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="family_agent", prompt_name="family", **kwargs)
