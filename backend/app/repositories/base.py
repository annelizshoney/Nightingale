from typing import Any


class BaseRepository:
    def __init__(self, session: Any | None = None) -> None:
        self.session = session
