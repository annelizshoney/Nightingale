from typing import Any


class BaseAgent:
    def __init__(self, service: Any | None = None) -> None:
        self.service = service

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        del args, kwargs
        raise NotImplementedError("Agent implementation is not available yet.")
