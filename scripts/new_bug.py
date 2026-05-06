"""Scaffold a new bug directory under bugs/<id>/."""
import argparse
import json
import sys
from pathlib import Path

BUGS_DIR = Path(__file__).parent.parent / "bugs"

CONFTEST = """\
import sys
from pathlib import Path

sys.modules.pop("buggy", None)
sys.path.insert(0, str(Path(__file__).parent.parent))
"""

TEST_STUB = """\
import buggy


def test_placeholder():
    # TODO: replace with real tests that fail on buggy.py and pass on the fix
    assert False, "not implemented"
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a new bug directory.")
    parser.add_argument("--id", dest="bug_id", required=True, help="Bug ID, e.g. py-off-by-one-011")
    parser.add_argument("--language", default="python")
    parser.add_argument("--category", required=True, help="off-by-one | logic | type-error | null-dereference | ...")
    parser.add_argument("--difficulty", default="easy", choices=["easy", "medium", "hard"])
    parser.add_argument("--description", default="", help="One-line description of the bug")
    args = parser.parse_args()

    bug_dir = BUGS_DIR / args.bug_id
    if bug_dir.exists():
        print(f"Error: {bug_dir} already exists.", file=sys.stderr)
        sys.exit(1)

    tests_dir = bug_dir / "tests"
    tests_dir.mkdir(parents=True)

    (bug_dir / "metadata.json").write_text(
        json.dumps(
            {
                "id": args.bug_id,
                "language": args.language,
                "category": args.category,
                "difficulty": args.difficulty,
                "description": args.description,
                "entrypoint": "buggy.py",
            },
            indent=2,
        )
        + "\n"
    )
    (bug_dir / "buggy.py").write_text("# TODO: add buggy code here\n")
    (bug_dir / "solution.patch").write_text("# TODO: unified diff patch (diff -u buggy.py fixed.py)\n")
    (tests_dir / "conftest.py").write_text(CONFTEST)
    (tests_dir / "test_fix.py").write_text(TEST_STUB)

    print(f"Scaffolded {bug_dir}/")
    print(f"  1. Fill in buggy.py with the broken code")
    print(f"  2. Fill in tests/test_fix.py with tests that fail on buggy, pass on fixed")
    print(f"  3. Generate solution.patch:  diff -u buggy.py fixed.py > solution.patch")
    print(f"  4. Verify:  python scripts/verify_bug.py {bug_dir}")


if __name__ == "__main__":
    main()
