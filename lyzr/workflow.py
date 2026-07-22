from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, Field

from app.lyzr.agent_registry import AgentRegistry


class WorkflowStepResult(BaseModel):
    step: str
    agent: str
    output: dict[str, Any] = Field(default_factory=dict)


class WorkflowExecution(BaseModel):
    request: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    steps: list[WorkflowStepResult] = Field(default_factory=list)


@dataclass(slots=True)
class WorkflowStep:
    name: str
    agent_name: str


@dataclass(slots=True)
class NightingaleWorkflow:
    registry: AgentRegistry
    core_steps: tuple[WorkflowStep, ...] = field(
        default_factory=lambda: (
            WorkflowStep(name="memory", agent_name="memory"),
            WorkflowStep(name="health", agent_name="health"),
            WorkflowStep(name="medication", agent_name="medication"),
            WorkflowStep(name="emergency", agent_name="emergency"),
            WorkflowStep(name="doctor", agent_name="doctor"),
            WorkflowStep(name="family", agent_name="family"),
        )
    )
    support_steps: tuple[WorkflowStep, ...] = field(
        default_factory=lambda: (
            WorkflowStep(name="routine", agent_name="routine"),
            WorkflowStep(name="appointment", agent_name="appointment"),
        )
    )

    def _step_input(
        self,
        *,
        request: str,
        metadata: dict[str, Any],
        step_name: str,
        previous_steps: list[WorkflowStepResult],
    ) -> dict[str, Any]:
        return {
            "user_request": request,
            "metadata": metadata,
            "current_step": step_name,
            "previous_steps": [step.model_dump(mode="json") for step in previous_steps],
        }

    def execute(
        self,
        request: str,
        metadata: dict[str, Any] | None = None,
        *,
        include_support_steps: bool = False,
    ) -> WorkflowExecution:
        execution = WorkflowExecution(request=request, metadata=metadata or {})
        ordered_steps = list(self.core_steps)
        if include_support_steps:
            ordered_steps.extend(self.support_steps)

        for step in ordered_steps:
            agent = self.registry.get(step.agent_name)
            step_input = self._step_input(
                request=request,
                metadata=execution.metadata,
                step_name=step.name,
                previous_steps=execution.steps,
            )
            output = agent.generate(step_input)
            execution.steps.append(
                WorkflowStepResult(step=step.name, agent=step.agent_name, output=output)
            )

        return execution
