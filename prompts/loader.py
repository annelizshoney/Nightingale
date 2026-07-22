from pathlib import Path


class PromptRepository:
    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parent

    def load(self, prompt_name: str) -> str:
        prompt_path = self.base_path / f"{prompt_name}.md"
        return prompt_path.read_text(encoding="utf-8").strip()

    def compose(self, *prompt_names: str, **format_values: str) -> str:
        parts = [self.load(name) for name in prompt_names]
        prompt = "\n\n".join(part for part in parts if part)
        if format_values:
            return prompt.format(**format_values)
        return prompt
