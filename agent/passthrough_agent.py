from pathlib import Path

from agent.base import Agent


class PassthroughAgent(Agent):
    def __init__(self, model: str | None = None) -> None:
        pass

    def fix(self, bug_dir: Path) -> str:
        return (bug_dir / "solution.patch").read_text()
