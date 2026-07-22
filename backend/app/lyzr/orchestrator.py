from __future__ import annotations

import asyncio
import json
from typing import Any, AsyncIterator

from app.lyzr.agent_registry import AgentRegistry
from app.lyzr.client import LyzrClient
from app.lyzr.workflow import NightingaleWorkflow, WorkflowExecution
from app.prompts.loader import PromptRepository


class LyzrOrchestrator:
    def __init__(
        self,
        *,
        registry: AgentRegistry,
        workflow: NightingaleWorkflow | None = None,
        client: LyzrClient | None = None,
        prompts: PromptRepository | None = None,
    ) -> None:
        self.registry = registry
        self.workflow = workflow or NightingaleWorkflow(registry=registry)
        self.client = client or LyzrClient()
        self.prompts = prompts or PromptRepository()
        self.system_prompt = self.prompts.compose("base", "orchestrator", agent_name="lyzr_orchestrator")

    def _finalize(self, execution: WorkflowExecution) -> dict[str, Any]:
        user_prompt = json.dumps(
            {
                "request": execution.request,
                "metadata": execution.metadata,
                "steps": [step.model_dump(mode="json") for step in execution.steps],
            },
            ensure_ascii=True,
        )
        final_response = self.client.generate_json(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )
        final_response.setdefault("request", execution.request)
        final_response.setdefault("metadata", execution.metadata)
        final_response.setdefault(
            "step_results",
            {step.step: step.output for step in execution.steps},
        )
        return final_response

    def run(
        self,
        request: str,
        metadata: dict[str, Any] | None = None,
        *,
        include_support_steps: bool = False,
    ) -> dict[str, Any]:
        execution = self.workflow.execute(
            request=request,
            metadata=metadata,
            include_support_steps=include_support_steps,
        )
        return self._finalize(execution)

    async def stream(
        self,
        request: str,
        metadata: dict[str, Any] | None = None,
        *,
        include_support_steps: bool = False,
    ) -> AsyncIterator[dict[str, Any]]:
        execution = await asyncio.to_thread(
            lambda: self.workflow.execute(
                request=request,
                metadata=metadata,
                include_support_steps=include_support_steps,
            ),
        )
        for step in execution.steps:
            yield {"type": "step", "step": step.step, "agent": step.agent, "output": step.output}
        yield {"type": "final", "output": self._finalize(execution)}

    def generate(
        self,
        request: str,
        metadata: dict[str, Any] | None = None,
        *,
        include_support_steps: bool = False,
    ) -> dict[str, Any]:
        return self.run(
            request=request,
            metadata=metadata,
            include_support_steps=include_support_steps,
        )
