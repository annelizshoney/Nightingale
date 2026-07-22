from __future__ import annotations

import asyncio
import json
from abc import ABC
from typing import Any, AsyncIterator, Iterator

from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

from app.adk.client import ADKClient
from app.adk.schemas import AgentEnvelope
from app.prompts.loader import PromptRepository


class BaseAgent(ABC):
    def __init__(
        self,
        *,
        name: str,
        prompt_name: str,
        client: ADKClient | None = None,
        prompts: PromptRepository | None = None,
    ) -> None:
        self.name = name
        self.prompt_name = prompt_name
        self._client = client or ADKClient()
        self._prompts = prompts or PromptRepository()
        self._instruction = self._prompts.compose("base", prompt_name, agent_name=name)
        self._agent: Agent = self._client.create_agent(
            name=name,
            instruction=self._instruction,
        )
        self._runner: InMemoryRunner = self._client.create_runner(self._agent)

    def _to_content(self, input_text: str | dict[str, Any] | AgentEnvelope) -> types.Content:
        if isinstance(input_text, AgentEnvelope):
            payload = input_text.model_dump(mode="json")
        elif isinstance(input_text, dict):
            payload = input_text
        else:
            payload = {"input": input_text}
        return types.UserContent(parts=[types.Part(text=json.dumps(payload, ensure_ascii=True))])

    def _extract_text(self, event: Any) -> str:
        content = getattr(event, "content", None)
        if not content or not getattr(content, "parts", None):
            return ""
        texts = [part.text for part in content.parts if getattr(part, "text", None)]
        return "\n".join(texts).strip()

    def _normalize_response(self, text: str) -> dict[str, Any]:
        if not text:
            return AgentEnvelope(agent=self.name, status="success").model_dump(mode="json")

        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3].strip()

        try:
            response = json.loads(cleaned)
        except json.JSONDecodeError:
            response = {"message": cleaned}

        if not isinstance(response, dict):
            response = {"data": response}

        response.setdefault("agent", self.name)
        response.setdefault("status", "success")
        response.setdefault("message", "")
        response.setdefault("data", {})
        response.setdefault("metadata", {})
        return response

    def run(self, input_text: str | dict[str, Any] | AgentEnvelope) -> dict[str, Any]:
        events = list(
            self._runner.run(
                user_id=self.name,
                session_id=f"{self.name}-session",
                new_message=self._to_content(input_text),
            )
        )
        for event in reversed(events):
            text = self._extract_text(event)
            if text:
                return self._normalize_response(text)
        return self._normalize_response("")

    async def stream(self, input_text: str | dict[str, Any] | AgentEnvelope) -> AsyncIterator[dict[str, Any]]:
        events = await asyncio.to_thread(
            lambda: list(
                self._runner.run(
                    user_id=self.name,
                    session_id=f"{self.name}-session",
                    new_message=self._to_content(input_text),
                )
            )
        )
        for event in events:
            if hasattr(event, "model_dump"):
                yield event.model_dump(exclude_none=True, mode="json")
            else:
                yield {"event": str(event)}

    def generate(self, input_text: str | dict[str, Any] | AgentEnvelope) -> dict[str, Any]:
        return self.run(input_text)
