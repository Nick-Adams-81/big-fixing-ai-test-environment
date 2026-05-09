from abc import ABC, abstractmethod
from pathlib import Path


class Agent(ABC):
    @abstractmethod
    def fix(self, bug_dir: Path) -> str:
        """Given a bug directory, return a unified diff patch string."""
