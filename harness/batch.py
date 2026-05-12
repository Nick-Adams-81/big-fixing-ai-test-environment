import argparse
import json
import time
from datetime import datetime
from pathlib import Path

from harness.report import report
from harness.runner import AGENTS, run

RUNS_INDEX = Path("results/runs.json")


def _auto_run_id(agent: str, model: str | None) -> str:
    slug = (model or "default").replace("/", "-").replace(":", "-")
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{agent}-{slug}-{ts}"


def _update_runs_index(entry: dict) -> None:
    RUNS_INDEX.parent.mkdir(parents=True, exist_ok=True)
    entries = json.loads(RUNS_INDEX.read_text()) if RUNS_INDEX.exists() else []
    entries.append(entry)
    RUNS_INDEX.write_text(json.dumps(entries, indent=2))


def batch(bugs_dir: Path, agent_name: str, output_dir: Path, model: str | None = None, run_id: str | None = None) -> None:
    bug_dirs = sorted(p for p in bugs_dir.iterdir() if p.is_dir())
    if not bug_dirs:
        raise SystemExit(f"No bug directories found in {bugs_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    timestamp = datetime.now().isoformat()
    start = time.monotonic()

    for bug_dir in bug_dirs:
        record = run(bug_dir, agent_name, output_dir, model=model)
        records.append(record)

    elapsed = time.monotonic() - start
    total_bugs = len(records)
    total_passed = sum(1 for r in records if r["all_passed"])
    total_input_tokens = sum(r["input_tokens"] or 0 for r in records)
    total_output_tokens = sum(r["output_tokens"] or 0 for r in records)
    avg_latency = sum(r["latency_seconds"] for r in records) / total_bugs
    resolved_model = records[0].get("model") if records else model

    summary = {
        "run_id": run_id,
        "timestamp": timestamp,
        "agent": agent_name,
        "model": resolved_model,
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

    _update_runs_index({
        "run_id": run_id,
        "agent": agent_name,
        "model": resolved_model,
        "timestamp": timestamp,
        "pass_rate": summary["pass_rate"],
        "bugs_passed": total_passed,
        "total_bugs": total_bugs,
        "output_dir": str(output_dir),
    })

    report(summary_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an agent against all bugs.")
    parser.add_argument("--bugs", type=Path, default=Path("bugs"), help="Bug corpus directory")
    parser.add_argument("--agent", required=True, choices=list(AGENTS), help="Agent to use")
    parser.add_argument("--model", default=None, help="Model override (e.g. claude-opus-4-7, gpt-4o-mini)")
    parser.add_argument("--run-id", default=None, dest="run_id", help="Named run ID (auto-generated if omitted)")
    parser.add_argument("--output", type=Path, default=None, help="Output directory (defaults to results/<run-id>/)")
    args = parser.parse_args()

    run_id = args.run_id or _auto_run_id(args.agent, args.model)
    output_dir = args.output or Path("results") / run_id

    batch(args.bugs, args.agent, output_dir, model=args.model, run_id=run_id)


if __name__ == "__main__":
    main()
