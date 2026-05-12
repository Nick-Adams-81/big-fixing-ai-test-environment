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

## Supported languages

| Language | Test runner | Bug naming |
|---|---|---|
| Python | pytest | `py-<category>-<id>` |
| TypeScript | vitest | `ts-<category>-<id>` |
| Go | `go test` | `go-<category>-<id>` |

The sandbox auto-detects the language from `metadata.json` and runs the appropriate test runner. No configuration needed.

---

## High-level architecture

```
bugs/
  <id>/
    buggy.py / buggy.ts / buggy.go   # the broken file
    tests/                            # test suite (Python, TypeScript)
    buggy_test.go                     # test suite (Go — lives alongside source)
    metadata.json                     # language, category, difficulty, description
    solution.patch                    # ground-truth fix (used for scoring, not given to agent)

agent/
  base.py             # Agent abstract interface
  claude_agent.py     # Claude API implementation
  ...                 # pluggable — swap in any model

harness/
  runner.py           # orchestrates agent + sandbox + evaluator for one bug
  sandbox.py          # Docker-based isolated execution (Python/TypeScript/Go)
  evaluator.py        # applies patch, runs tests, produces pass/fail + metrics
  batch.py            # runs the full benchmark suite, collects aggregate stats
  report.py           # prints a formatted results table from summary.json

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

## Agents

| Agent | `--agent` value | Default model | Notes |
|---|---|---|---|
| Passthrough | `passthrough` | — | Returns ground-truth patch; used for CI and sanity checks |
| Claude | `claude` | `claude-sonnet-4-6` | Uses extended thinking; supports multi-turn retry loop |
| OpenAI | `openai` | `gpt-4o` | Optional — see below |

### Selecting a model

Use `--model` to override the default for any agent:

```bash
python -m harness.runner bugs/py-logic-001 --agent claude --model claude-opus-4-7
python -m harness.runner bugs/py-logic-001 --agent openai --model gpt-4o-mini
```

The model name is recorded in every result JSON and shown in the batch report header.

### OpenAI agent (optional)

The OpenAI agent is not installed by default. To use it:

```bash
pip install openai
# Add OPENAI_API_KEY=<your-key> to .env
python -m harness.runner bugs/py-logic-001 --agent openai
```

### Agent interface

Agents implement two methods:

```python
class Agent:
    def fix(self, bug_dir: Path) -> str:
        """Return a unified diff patch string."""

    def retry(self, test_output: str) -> str:
        """Given test failure output, return a revised patch (optional)."""
```

The harness calls `fix()`, evaluates the patch, and if tests fail calls `retry()` with the failure output up to 3 times. Agents that don't support retry return `""` from `retry()` and the loop stops.

---

## Evaluation metrics

| Metric | Description |
|---|---|
| Pass rate | % of bugs where all tests pass after the patch |
| Partial credit | % of tests passing (when full pass isn't achieved) |
| Latency | Wall-clock seconds for the agent to produce a patch |
| Token usage | Input/output tokens consumed (Claude agents) |

---

## Prerequisites

- Python 3.11+
- [Docker](https://docs.docker.com/get-docker/) — required for sandboxed test execution

Build the sandbox image once before running anything:

```bash
docker build -t bug-fixer-sandbox:latest -f docker/Dockerfile docker/
```

The image includes Python (pytest), Node.js (vitest), and Go — all three language runtimes in one image. It is reused across all runs. The harness will also build it automatically on first use if it doesn't exist.

---

## Quickstart

```bash
# Install dependencies
pip install -r requirements.txt

# Copy .env and add your Anthropic API key
cp .env.example .env   # then edit .env

# Run the Claude agent against a single bug
python -m harness.runner bugs/py-off-by-one-001 --agent claude

# Run against a TypeScript bug
python -m harness.runner bugs/ts-logic-001 --agent claude

# Run against a Go bug
python -m harness.runner bugs/go-off-by-one-001 --agent claude

# Run the full benchmark suite (all 50 bugs)
python -m harness.batch --agent claude --output results/my-run/

# Run only Python bugs
for d in bugs/py-*/; do python -m harness.runner "$d" --agent claude; done

# Run only TypeScript bugs
for d in bugs/ts-*/; do python -m harness.runner "$d" --agent claude; done

# Run only Go bugs
for d in bugs/go-*/; do python -m harness.runner "$d" --agent claude; done

# View a saved report
python -m harness.report results/my-run/summary.json

# Export corpus as JSONL for fine-tuning
python scripts/export_dataset.py --output dataset.jsonl
```

---

## Adding a new bug

```bash
python scripts/new_bug.py --id py-logic-010 --language python --category logic
# scaffolds bugs/py-logic-010/ with empty buggy.py, tests/, and metadata.json
```

Fill in the buggy source file, write tests that fail on it, then verify:

```bash
python scripts/verify_bug.py bugs/py-logic-010
# checks: tests fail on buggy, tests pass on ground-truth patch
```

---

## Project structure

```
.
├── bugs/               # bug corpus (50 bugs: Python, TypeScript, Go)
├── agent/              # agent implementations
├── harness/            # runner, sandbox, evaluator, batch runner, report
├── scripts/            # dev utilities (new_bug, verify_bug, export_dataset, generate_corpus)
├── docker/             # Dockerfile and package.json for the sandbox image
├── results/            # benchmark run outputs (gitignored)
├── .github/workflows/  # CI: verify all bugs on every push
├── requirements.txt
└── README.md
```

---

## CI

Every push and pull request runs `.github/workflows/verify-corpus.yml`, which builds the sandbox image and runs the passthrough agent against all 50 bugs. The workflow fails if any bug drops below 100%.

---

## Roadmap

See `TODO.md` for the full phased build plan.
