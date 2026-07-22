from typing import Any

from pydantic import BaseModel, Field


class AgentEnvelope(BaseModel):
    agent: str = Field(default="")
    status: str = Field(default="success")
    message: str = Field(default="")
    data: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
