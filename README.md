# Bug Fixer Frontier — Agent Training & Evaluation Environment

A self-contained environment for training, testing, and benchmarking AI coding agents that automatically find and fix bugs in code.

---

## What it is

This repo provides a structured harness for running a coding agent against a curated dataset of buggy programs. Given a buggy file and (optionally) a failing test suite, the agent produces a patch. The harness executes the patch in an isolated sandbox, runs the tests, and records whether the bug was fixed.

The goal is to make it easy to:
- Benchmark different models / prompting strategies against a consistent bug corpus
- Generate training data (bug → fix pairs) for fine-tuning
- Run iterative prompt or agent-loop experiments without re-wiring evaluation each time

---

## High-level architecture

```
bugs/
  <id>/
    buggy.py          # the broken file
    tests/            # test suite that fails on buggy, passes on fixed
    metadata.json     # language, category, difficulty, description
    solution.patch    # ground-truth fix (used for scoring, not given to agent)

agent/
  base.py             # Agent abstract interface
  claude_agent.py     # Claude API implementation
  ...                 # pluggable — swap in any model

harness/
  runner.py           # orchestrates agent + sandbox + evaluator for one bug
  sandbox.py          # Docker-based isolated execution
  evaluator.py        # runs tests, diffs output, produces pass/fail + metrics
  batch.py            # runs the full benchmark suite, collects aggregate stats

results/
  <run-id>/
    summary.json      # aggregate metrics
    <bug-id>.json     # per-bug result: patch produced, tests passed, latency
```

---

## Bug dataset format

Each bug lives in `bugs/<id>/`. The `metadata.json` schema:

```json
{
  "id": "py-off-by-one-001",
  "language": "python",
  "category": "off-by-one",
  "difficulty": "easy",
  "description": "Loop iterates one element past the end of the list.",
  "entrypoint": "buggy.py"
}
```

Categories include: `off-by-one`, `null-dereference`, `type-error`, `logic`, `concurrency`, `resource-leak`, `security`.

---

## Agent interface

Agents implement a single method:

```python
class Agent:
    def fix(self, bug_dir: Path) -> str:
        """Return a unified diff patch string."""
```

The harness calls `fix()`, applies the patch, runs the tests, and scores the result. Swapping agents is one line.

---

## Evaluation metrics

| Metric | Description |
|---|---|
| Pass rate | % of bugs where all tests pass after the patch |
| Partial credit | % of tests passing (when full pass isn't achieved) |
| Exact match | Patch is semantically equivalent to ground-truth solution |
| Latency | Wall-clock seconds per bug |
| Token usage | Input/output tokens consumed (Claude agents) |

---

## Quickstart

```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent against a single bug
python -m harness.runner bugs/py-off-by-one-001 --agent claude

# Run the full benchmark suite
python -m harness.batch --agent claude --output results/my-run/

# View results
python -m harness.report results/my-run/summary.json
```

---

## Adding a new bug

```bash
python scripts/new_bug.py --id py-logic-007 --language python --category logic
# scaffolds bugs/py-logic-007/ with empty buggy.py, tests/, and metadata.json
```

Fill in `buggy.py` with the broken code, write tests that fail on it, then run:

```bash
python scripts/verify_bug.py bugs/py-logic-007
# checks: tests fail on buggy, tests pass on ground-truth patch
```

---

## Project structure

```
.
├── bugs/               # bug corpus
├── agent/              # agent implementations
├── harness/            # runner, sandbox, evaluator, batch runner
├── scripts/            # dev utilities (new_bug, verify_bug, export_dataset)
├── results/            # benchmark run outputs (gitignored)
├── requirements.txt
└── README.md
```

---

## Roadmap

See `TODO.md` for the full phased build plan.
