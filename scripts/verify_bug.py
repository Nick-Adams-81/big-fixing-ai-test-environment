"""Verify a bug entry: tests must fail on buggy.py and pass after solution.patch is applied."""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run_pytest(tests_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "pytest", str(tests_dir), "-q", "--tb=short"],
        capture_output=True,
        text=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify a bug directory.")
    parser.add_argument("bug_dir", type=Path, help="Path to the bug directory, e.g. bugs/py-off-by-one-001")
    args = parser.parse_args()

    bug_dir: Path = args.bug_dir.resolve()
    buggy_file = bug_dir / "buggy.py"
    patch_file = bug_dir / "solution.patch"
    tests_dir = bug_dir / "tests"

    for required in (buggy_file, patch_file, tests_dir):
        if not required.exists():
            print(f"Error: {required} not found.", file=sys.stderr)
            sys.exit(1)

    print(f"Verifying {bug_dir.name}...")

    # Step 1: tests must FAIL on the original buggy code
    print("\n[1/2] Tests against buggy code (expect at least one failure)...")
    result = run_pytest(tests_dir)
    if result.returncode == 0:
        print("  FAIL — all tests passed on buggy code; the bug is not caught.")
        print(result.stdout)
        sys.exit(1)
    print("  OK — tests fail as expected.")

    # Step 2: apply patch to a temp copy, tests must all PASS
    print("\n[2/2] Tests against patched code (expect all to pass)...")
    with tempfile.TemporaryDirectory() as tmp:
        patched_dir = Path(tmp) / bug_dir.name
        shutil.copytree(bug_dir, patched_dir)
        patched_buggy = patched_dir / "buggy.py"

        patch_proc = subprocess.run(
            ["patch", str(patched_buggy)],
            input=patch_file.read_text(),
            capture_output=True,
            text=True,
        )
        if patch_proc.returncode != 0:
            print("  FAIL — patch did not apply cleanly.")
            print(patch_proc.stderr, file=sys.stderr)
            sys.exit(1)

        result = run_pytest(patched_dir / "tests")
        if result.returncode != 0:
            print("  FAIL — tests still failing after patch.")
            print(result.stdout)
            sys.exit(1)
        print("  OK — all tests pass after patch.")

    print(f"\n{bug_dir.name}: verified.")


if __name__ == "__main__":
    main()
