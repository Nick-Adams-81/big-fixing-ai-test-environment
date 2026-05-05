# Build Gameplan

Phased plan for building the bug-fixer agent training & evaluation environment.

---

## Phase 1 — Project scaffold & bug corpus format

Goal: a repo you can actually run something against.

- [ ] Set up Python project (`pyproject.toml` or `setup.py`, `requirements.txt`)
- [ ] Define `bugs/<id>/` directory structure and `metadata.json` schema
- [ ] Write `scripts/new_bug.py` — scaffolds a new bug directory
- [ ] Write `scripts/verify_bug.py` — asserts tests fail on buggy, pass on fix
- [ ] Seed the corpus with **10 hand-crafted bugs** across 3–4 categories (off-by-one, type-error, logic, null-dereference) in Python
- [ ] Add `.gitignore` (exclude `results/`, `__pycache__`, `.env`)

**Done when:** `verify_bug.py bugs/<id>` runs cleanly on all 10 seed bugs.

---

## Phase 2 — Harness core (single-bug runner)

Goal: the harness can run any agent against a single bug and produce a result.

- [ ] `harness/evaluator.py` — applies a patch to a temp copy of `buggy.py`, runs the test suite, returns pass/fail counts
- [ ] `harness/runner.py` — wires bug dir + agent + evaluator, writes `<bug-id>.json` result
- [ ] Stub `agent/base.py` with the `Agent` abstract interface
- [ ] Implement `agent/passthrough_agent.py` — returns the ground-truth patch (sanity-check that evaluator works)
- [ ] CLI: `python -m harness.runner bugs/<id> --agent passthrough`

**Done when:** passthrough agent scores 100% on all 10 seed bugs.

---

## Phase 3 — Sandboxed execution

Goal: code runs in isolation so a buggy or malicious patch can't affect the host.

- [ ] `harness/sandbox.py` — Docker-based executor; mounts bug dir read-only, runs tests in container, returns stdout/stderr/exit code
- [ ] Choose a base Docker image (e.g., `python:3.12-slim`)
- [ ] Add timeout enforcement (default 30s per bug)
- [ ] Wire sandbox into `runner.py` (replace direct subprocess calls)
- [ ] Document Docker dependency in README quickstart

**Done when:** runner works end-to-end with sandbox on the 10 seed bugs.

---

## Phase 4 — Claude agent

Goal: a real LLM agent that reads buggy code and produces a patch.

- [ ] Add `anthropic` SDK to requirements
- [ ] `agent/claude_agent.py` implementing the `Agent` interface
- [ ] Prompt v1: system prompt + full buggy file + test failures → ask for unified diff
- [ ] Handle common failure modes: agent returns prose instead of diff, malformed patch
- [ ] Log token usage per call into the result JSON
- [ ] Run Claude agent against all 10 seed bugs; record baseline pass rate

**Done when:** Claude agent produces a valid patch (even if wrong) for every bug, and pass rate is recorded.

---

## Phase 5 — Batch runner & reporting

Goal: run the full corpus in one command and get aggregate stats.

- [ ] `harness/batch.py` — iterates all bugs, calls runner, collects results into `results/<run-id>/`
- [ ] `harness/report.py` — reads `summary.json`, prints a table: pass rate, partial credit, avg latency, total tokens
- [ ] Write `results/` to `.gitignore`
- [ ] CLI: `python -m harness.batch --agent claude --output results/my-run/`
- [ ] CLI: `python -m harness.report results/my-run/summary.json`

**Done when:** a full batch run completes and prints a readable report.

---

## Phase 6 — Corpus expansion

Goal: enough bugs to meaningfully differentiate agents.

- [ ] Expand corpus to **50 bugs** across Python, JavaScript, and one compiled language (Go or Rust)
- [ ] Add difficulty levels (easy / medium / hard) to metadata; balance the corpus
- [ ] Add `scripts/export_dataset.py` — exports corpus as JSONL for fine-tuning pipelines
- [ ] Validate every bug with `verify_bug.py` in CI (GitHub Actions)

**Done when:** CI passes on 50 verified bugs; JSONL export works.

---

## Phase 7 — Prompt & agent iteration

Goal: systematically improve the agent's pass rate.

- [ ] Add multi-turn agent loop: agent can read test output and retry (up to N attempts)
- [ ] Experiment with chain-of-thought reasoning before producing the patch
- [ ] Try providing git diff context (surrounding lines) vs. full file
- [ ] Add `agent/openai_agent.py` as a comparison baseline
- [ ] Log all experiments to `results/` with a named run ID for reproducibility

**Done when:** best agent configuration is documented with its pass rate on the full corpus.

---

## Phase 8 — Fine-tuning data pipeline (optional / future)

Goal: use the corpus to generate training data for a smaller specialized model.

- [ ] Generate synthetic bug variants from correct code (mutation testing approach)
- [ ] `scripts/generate_synthetic_bugs.py` — applies common mutation operators (flip comparison, swap +/-, drop None check)
- [ ] Verify synthetic bugs with `verify_bug.py`
- [ ] Export fine-tuning JSONL: `{ "prompt": <buggy + tests>, "completion": <patch> }`
- [ ] Document fine-tuning workflow (Anthropic fine-tuning API or HuggingFace)

---

## Ongoing / hygiene

- [ ] Add `pytest` suite for the harness itself (unit-test evaluator, runner, sandbox)
- [ ] Type-annotate all harness modules (`mypy` clean)
- [ ] Pre-commit hooks: `black`, `ruff`, `mypy`
- [ ] Write `CONTRIBUTING.md` with instructions for adding bugs
