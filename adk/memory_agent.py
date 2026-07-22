from app.adk.base_agent import BaseAgent


class MemoryAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="memory_agent", prompt_name="memory", **kwargs)
