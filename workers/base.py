from typing import Any


class BaseWorker:
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        del args, kwargs
        raise NotImplementedError("Worker implementation is not available yet.")
