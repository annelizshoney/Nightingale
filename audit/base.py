from typing import Any


class AuditTrail:
    def __init__(self, store: Any | None = None) -> None:
        self.store = store
