import argparse
import json
import time
from pathlib import Path

from harness.report import report
from harness.runner import AGENTS, run


def batch(bugs_dir: Path, agent_name: str, output_dir: Path) -> None:
    bug_dirs = sorted(p for p in bugs_dir.iterdir() if p.is_dir())
    if not bug_dirs:
        raise SystemExit(f"No bug directories found in {bugs_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    start = time.monotonic()

    for bug_dir in bug_dirs:
        record = run(bug_dir, agent_name, output_dir)
        records.append(record)

    elapsed = time.monotonic() - start
    total_bugs = len(records)
    total_passed = sum(1 for r in records if r["all_passed"])
    total_input_tokens = sum(r["input_tokens"] or 0 for r in records)
    total_output_tokens = sum(r["output_tokens"] or 0 for r in records)
    avg_latency = sum(r["latency_seconds"] for r in records) / total_bugs

    summary = {
        "agent": agent_name,
        "total_bugs": total_bugs,
        "bugs_passed": total_passed,
        "pass_rate": round(total_passed / total_bugs, 4),
        "avg_latency_seconds": round(avg_latency, 3),
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "wall_seconds": round(elapsed, 3),
        "results": records,
    }

    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    report(summary_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an agent against all bugs.")
    parser.add_argument("--bugs", type=Path, default=Path("bugs"), help="Bug corpus directory")
    parser.add_argument("--agent", required=True, choices=list(AGENTS), help="Agent to use")
    parser.add_argument("--output", type=Path, default=Path("results/latest"), help="Directory to write results")
    args = parser.parse_args()

    batch(args.bugs, args.agent, args.output)


if __name__ == "__main__":
    main()
