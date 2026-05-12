import argparse
import json
from pathlib import Path


def export(bugs_dir: Path, output_path: Path) -> None:
    bug_dirs = sorted(p for p in bugs_dir.iterdir() if p.is_dir())
    records = []

    for bug_dir in bug_dirs:
        meta_file = bug_dir / "metadata.json"
        if not meta_file.exists():
            continue

        metadata = json.loads(meta_file.read_text())
        entrypoint = metadata.get("entrypoint", "buggy.py")
        language = metadata.get("language", "python")

        buggy_code = (bug_dir / entrypoint).read_text()
        patch = (bug_dir / "solution.patch").read_text()

        if language == "go":
            test_files = sorted(bug_dir.glob("*_test.go"))
        else:
            test_files = sorted((bug_dir / "tests").glob("test_fix*"))

        tests = "\n\n".join(f.read_text() for f in test_files)

        records.append({
            "id": metadata["id"],
            "language": language,
            "category": metadata.get("category", ""),
            "difficulty": metadata.get("difficulty", ""),
            "description": metadata.get("description", ""),
            "buggy": buggy_code,
            "tests": tests,
            "patch": patch,
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    print(f"Exported {len(records)} bugs to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export bug corpus as JSONL.")
    parser.add_argument("--bugs", type=Path, default=Path("bugs"), help="Bug corpus directory")
    parser.add_argument("--output", type=Path, default=Path("dataset.jsonl"), help="Output JSONL file")
    args = parser.parse_args()

    export(args.bugs, args.output)


if __name__ == "__main__":
    main()
