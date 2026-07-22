from app.adk.base_agent import BaseAgent


class RoutineAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="routine_agent", prompt_name="routine", **kwargs)
