from __future__ import annotations

import os

from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

from app.adk.schemas import AgentEnvelope


class ADKClient:
    model_name = "gemini-2.5-flash"

    def __init__(self, api_key: str | None = None, app_name: str = "Nightingale") -> None:
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY must be set in the environment.")
        os.environ["GOOGLE_API_KEY"] = self.api_key
        self.app_name = app_name

    def create_agent(self, *, name: str, instruction: str) -> Agent:
        return Agent(
            name=name,
            model=self.model_name,
            mode="chat",
            instruction=instruction,
            output_schema=AgentEnvelope,
            generate_content_config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )

    def create_runner(self, agent: Agent) -> InMemoryRunner:
        return InMemoryRunner(agent=agent, app_name=self.app_name)

    def health_check(self) -> dict[str, str]:
        return {
            "status": "ready",
            "model": self.model_name,
            "app_name": self.app_name,
        }

