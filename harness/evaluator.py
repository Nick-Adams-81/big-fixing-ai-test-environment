import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class EvalResult:
    passed: int
    failed: int
    errors: int

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
    passed = int(m.group(1)) if (m := re.search(r"(\d+) passed", output)) else 0
    failed = int(m.group(1)) if (m := re.search(r"(\d+) failed", output)) else 0
    errors = int(m.group(1)) if (m := re.search(r"(\d+) error", output)) else 0
    return passed, failed, errors


def evaluate(bug_dir: Path, patch: str) -> EvalResult:
    with tempfile.TemporaryDirectory() as tmp:
        patched_dir = Path(tmp) / bug_dir.name
        shutil.copytree(bug_dir, patched_dir)

        patch_proc = subprocess.run(
            ["patch", str(patched_dir / "buggy.py")],
            input=patch,
            capture_output=True,
            text=True,
        )
        if patch_proc.returncode != 0:
            return EvalResult(passed=0, failed=0, errors=1)

        pytest_proc = subprocess.run(
            [sys.executable, "-m", "pytest", str(patched_dir / "tests"), "-q", "--tb=no", "--no-header"],
            capture_output=True,
            text=True,
        )

        passed, failed, errors = _parse_counts(pytest_proc.stdout)
        return EvalResult(passed=passed, failed=failed, errors=errors)
