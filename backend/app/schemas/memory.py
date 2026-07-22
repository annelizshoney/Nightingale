from typing import Any

from pydantic import BaseModel, Field


class MemoryCreateRequest(BaseModel):
    text: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class MemoryItem(BaseModel):
    id: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    score: float | None = None


class MemorySearchResponse(BaseModel):
    items: list[MemoryItem]
