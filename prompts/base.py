from dataclasses import dataclass


@dataclass(slots=True)
class PromptTemplate:
    name: str = ""
    template: str = ""
