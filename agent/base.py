from abc import ABC, abstractmethod
from pathlib import Path


class Agent(ABC):
    @abstractmethod
    def fix(self, bug_dir: Path) -> str:
        """Given a bug directory, return a unified diff patch string."""

    def retry(self, test_output: str) -> str:
        """Given test failure output from the previous attempt, return a revised patch.

        Default implementation signals no retry support. Override in agents that
        maintain conversation history (e.g. ClaudeAgent).
        """
        return ""
