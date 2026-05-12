import argparse
import importlib
import json
import time
from pathlib import Path

from agent.base import Agent
from harness.evaluator import evaluate

AGENTS: dict[str, str] = {
    "passthrough": "agent.passthrough_agent.PassthroughAgent",
    "claude": "agent.claude_agent.ClaudeAgent",
}


def load_agent(name: str) -> Agent:
    if name not in AGENTS:
        raise ValueError(f"Unknown agent '{name}'. Available: {list(AGENTS)}")
    module_path, class_name = AGENTS[name].rsplit(".", 1)
    cls = getattr(importlib.import_module(module_path), class_name)
    return cls()


def run(bug_dir: Path, agent_name: str, output_dir: Path) -> dict:
    bug_dir = bug_dir.resolve()
    metadata = json.loads((bug_dir / "metadata.json").read_text())

    agent = load_agent(agent_name)

    start = time.monotonic()
    patch = agent.fix(bug_dir)
    latency = time.monotonic() - start

    result = evaluate(bug_dir, patch)

    record = {
        "bug_id": metadata["id"],
        "agent": agent_name,
        "patch": patch,
        "passed": result.passed,
        "failed": result.failed,
        "errors": result.errors,
        "total": result.total,
        "pass_rate": round(result.pass_rate, 4),
        "all_passed": result.all_passed,
        "latency_seconds": round(latency, 3),
        "input_tokens": getattr(agent, "input_tokens", None),
        "output_tokens": getattr(agent, "output_tokens", None),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{metadata['id']}.json").write_text(json.dumps(record, indent=2))

    status = "OK" if result.all_passed else "FAIL"
    print(f"{metadata['id']}: {result.passed}/{result.total} passed [{status}] ({latency:.2f}s)")

    return record


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an agent against a single bug.")
    parser.add_argument("bug_dir", type=Path, help="Path to the bug directory")
    parser.add_argument("--agent", required=True, choices=list(AGENTS), help="Agent to use")
    parser.add_argument("--output", type=Path, default=Path("results"), help="Directory to write result JSON")
    args = parser.parse_args()

    run(args.bug_dir, args.agent, args.output)


if __name__ == "__main__":
    main()
