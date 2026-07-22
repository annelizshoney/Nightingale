from typing import Any


class BaseIntegration:
    def __init__(self, client: Any | None = None) -> None:
        self.client = client
