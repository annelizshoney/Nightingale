from typing import Any


class BaseService:
    def __init__(self, repository: Any | None = None, integration: Any | None = None) -> None:
        self.repository = repository
        self.integration = integration

    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        del args, kwargs
        raise NotImplementedError("Service implementation is not available yet.")
