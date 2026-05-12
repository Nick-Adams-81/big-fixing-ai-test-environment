import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from agent.base import Agent
from agent.prompts import build_prompt, extract_patch, read_tests, system_prompt

load_dotenv()

DEFAULT_MODEL = "gpt-4o"
MAX_TOKENS = 2048


class OpenAIAgent(Agent):
    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self._client = OpenAI()
        self._model = model
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self._messages: list[dict] = []
        self._system: str = ""
        self._entrypoint: str = ""

    def fix(self, bug_dir: Path) -> str:
        metadata = json.loads((bug_dir / "metadata.json").read_text())
        language = metadata.get("language", "python")
        self._entrypoint = metadata.get("entrypoint", "buggy.py")

        buggy_code = (bug_dir / self._entrypoint).read_text()
        tests = read_tests(bug_dir, language)

        self._system = system_prompt(language)
        self._messages = [{"role": "user", "content": build_prompt(buggy_code, tests, self._entrypoint, language)}]
        self.input_tokens = 0
        self.output_tokens = 0

        return self._call()

    def retry(self, test_output: str) -> str:
        self._messages.append({
            "role": "user",
            "content": (
                "Your patch was applied but tests still failed. Here is the test output:\n\n"
                f"{test_output.strip()}\n\n"
                "Analyze the failures and produce a corrected unified diff patch."
            ),
        })
        return self._call()

    def _call(self) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "system", "content": self._system}] + self._messages,
        )
        text = response.choices[0].message.content or ""
        self._messages.append({"role": "assistant", "content": text})
        self.input_tokens += response.usage.prompt_tokens
        self.output_tokens += response.usage.completion_tokens
        return extract_patch(text, self._entrypoint)
