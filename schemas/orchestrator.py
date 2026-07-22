from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.schemas.agent import AgentRequest


class OrchestratorRequest(AgentRequest):
    include_support_steps: bool = False


class OrchestratorStepResult(BaseModel):
    step: str
    agent: str
    output: dict[str, Any] = Field(default_factory=dict)


class OrchestratorResponse(BaseModel):
    status: str = "success"
    summary: str = ""
    risk_level: str = "low"
    immediate_actions: list[str] = Field(default_factory=list)
    care_actions: list[str] = Field(default_factory=list)
    family_actions: list[str] = Field(default_factory=list)
    follow_up: list[str] = Field(default_factory=list)
    step_results: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    request: str = ""
