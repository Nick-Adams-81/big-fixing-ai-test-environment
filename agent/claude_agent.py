import re
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from agent.base import Agent

load_dotenv()

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024

_SYSTEM_PROMPT = """\
You are an expert software engineer specializing in debugging Python code.
You will be given a buggy Python file and its failing test suite.
Your task is to identify the bug and return a unified diff patch that fixes it.

Rules:
- Output ONLY the unified diff patch, nothing else — no explanation, no prose.
- Use exactly this header format:
  --- a/buggy.py
  +++ b/buggy.py
"""


def _build_prompt(buggy_code: str, tests: str) -> str:
    return (
        f"### buggy.py\n```python\n{buggy_code}\n```\n\n"
        f"### tests\n```python\n{tests}\n```\n\n"
        "Produce a unified diff patch to fix the bug in buggy.py."
    )


def _extract_patch(text: str) -> str:
    text = text.strip()
    if text.startswith("---"):
        return text + "\n"
    if m := re.search(r"```(?:diff|patch)?\n(.*?)```", text, re.DOTALL):
        return m.group(1).strip() + "\n"
    if m := re.search(r"(--- a/buggy\.py.*)", text, re.DOTALL):
        return m.group(1).strip() + "\n"
    return ""


class ClaudeAgent(Agent):
    def __init__(self) -> None:
        self._client = anthropic.Anthropic()
        self.input_tokens: int = 0
        self.output_tokens: int = 0

    def fix(self, bug_dir: Path) -> str:
        buggy_code = (bug_dir / "buggy.py").read_text()
        test_files = sorted((bug_dir / "tests").glob("test_*.py"))
        tests = "\n\n".join(f.read_text() for f in test_files)

        response = self._client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": _build_prompt(buggy_code, tests)}],
        )

        self.input_tokens = response.usage.input_tokens
        self.output_tokens = response.usage.output_tokens

        return _extract_patch(response.content[0].text)
