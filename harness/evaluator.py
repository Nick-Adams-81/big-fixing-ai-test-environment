import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from harness import sandbox


@dataclass
class EvalResult:
    passed: int
    failed: int
    errors: int
    test_output: str = ""

    @property
    def total(self) -> int:
        return self.passed + self.failed + self.errors

    @property
    def all_passed(self) -> bool:
        return self.total > 0 and self.failed == 0 and self.errors == 0

    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total > 0 else 0.0


def _parse_counts(output: str) -> tuple[int, int, int]:
    # go test -v output — identified by "=== RUN" lines
    if "=== RUN" in output:
        passed = len(re.findall(r"--- PASS:", output))
        failed = len(re.findall(r"--- FAIL:", output))
        return passed, failed, 0
    # vitest output — identified by "Test Files" summary line
    if "Test Files" in output:
        passed = int(m.group(1)) if (m := re.search(r"Tests\s+(?:\d+ failed \| )?(\d+) passed", output)) else 0
        failed = int(m.group(1)) if (m := re.search(r"Tests\s+(\d+) failed", output)) else 0
        return passed, failed, 0
    # pytest output
    passed = int(m.group(1)) if (m := re.search(r"(\d+) passed", output)) else 0
    failed = int(m.group(1)) if (m := re.search(r"(\d+) failed", output)) else 0
    errors = int(m.group(1)) if (m := re.search(r"(\d+) error", output)) else 0
    return passed, failed, errors


def evaluate(bug_dir: Path, patch: str) -> EvalResult:
    metadata = json.loads((bug_dir / "metadata.json").read_text())
    language = metadata.get("language", "python")
    entrypoint = metadata.get("entrypoint", "buggy.py")

    with tempfile.TemporaryDirectory() as tmp:
        patched_dir = Path(tmp) / bug_dir.name
        shutil.copytree(bug_dir, patched_dir)

        patch_proc = subprocess.run(
            ["patch", str(patched_dir / entrypoint)],
            input=patch,
            capture_output=True,
            text=True,
        )
        if patch_proc.returncode != 0:
            return EvalResult(passed=0, failed=0, errors=1)

        stdout, stderr, _ = sandbox.run_tests(patched_dir, language=language)
        passed, failed, errors = _parse_counts(stdout)
        return EvalResult(passed=passed, failed=failed, errors=errors, test_output=stdout or stderr)
