from __future__ import annotations

import importlib
import json
import os
from typing import Any


class LyzrClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        model_name: str = "gpt-4o-mini",
        model_type: str = "openai",
    ) -> None:
        self.api_key = api_key or os.getenv("LYZR_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("LYZR_API_KEY or OPENAI_API_KEY must be set in the environment.")
        self.model_name = model_name
        self.model_type = model_type

    def _get_llm(self) -> Any:
        try:
            llm_module = importlib.import_module("lyzr.base.llms")
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Lyzr is not installed. Install the lyzr package before using the orchestrator."
            ) from exc
        return llm_module.get_model(
            api_key=self.api_key,
            model_type=self.model_type,
            model_name=self.model_name,
        )

    @staticmethod
    def _extract_text(response: Any) -> str:
        choices = getattr(response, "choices", None)
        if choices:
            message = choices[0].message
            return (getattr(message, "content", None) or "").strip()
        if hasattr(response, "message"):
            return (getattr(response.message, "content", None) or "").strip()
        return str(response).strip()

    @staticmethod
    def _load_json(text: str) -> dict[str, Any]:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3].strip()
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            data = {"message": cleaned}
        if not isinstance(data, dict):
            data = {"data": data}
        return data

    def generate_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        top_p: float = 0.9,
    ) -> dict[str, Any]:
        llm = self._get_llm()
        response = llm.run(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            top_p=top_p,
            response_format={"type": "json_object"},
        )
        return self._load_json(self._extract_text(response))

    def health_check(self) -> dict[str, str]:
        return {
            "status": "ready",
            "model": self.model_name,
            "provider": self.model_type,
        }

