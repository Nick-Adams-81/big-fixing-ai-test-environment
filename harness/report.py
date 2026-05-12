import argparse
import json
from pathlib import Path


def report(summary_path: Path) -> None:
    summary = json.loads(summary_path.read_text())
    results = summary["results"]

    col_widths = {"bug_id": 24, "status": 8, "tests": 10, "att": 5, "latency": 10, "tokens_in": 10, "tokens_out": 11}
    header = (
        f"{'bug_id':<{col_widths['bug_id']}}"
        f"{'status':<{col_widths['status']}}"
        f"{'tests':<{col_widths['tests']}}"
        f"{'att':<{col_widths['att']}}"
        f"{'latency':<{col_widths['latency']}}"
        f"{'tokens_in':<{col_widths['tokens_in']}}"
        f"{'tokens_out':<{col_widths['tokens_out']}}"
    )
    divider = "-" * len(header)

    run_id_str = f"  run: {summary['run_id']}" if summary.get("run_id") else ""
    model_str = f"  model: {summary['model']}" if summary.get("model") else ""
    print(f"\nAgent: {summary['agent']}{model_str}{run_id_str}")
    print(divider)
    print(header)
    print(divider)

    for r in results:
        status = "OK" if r["all_passed"] else "FAIL"
        tests = f"{r['passed']}/{r['total']}"
        att = str(r.get("attempts", 1))
        latency = f"{r['latency_seconds']:.2f}s"
        tokens_in = str(r["input_tokens"]) if r["input_tokens"] is not None else "-"
        tokens_out = str(r["output_tokens"]) if r["output_tokens"] is not None else "-"
        print(
            f"{r['bug_id']:<{col_widths['bug_id']}}"
            f"{status:<{col_widths['status']}}"
            f"{tests:<{col_widths['tests']}}"
            f"{att:<{col_widths['att']}}"
            f"{latency:<{col_widths['latency']}}"
            f"{tokens_in:<{col_widths['tokens_in']}}"
            f"{tokens_out:<{col_widths['tokens_out']}}"
        )

    print(divider)
    pass_pct = summary["pass_rate"] * 100
    print(
        f"{'TOTAL':<{col_widths['bug_id']}}"
        f"{summary['bugs_passed']}/{summary['total_bugs']} passed ({pass_pct:.1f}%)"
    )
    print(f"avg latency: {summary['avg_latency_seconds']:.2f}s  |  "
          f"total tokens: {summary['total_input_tokens']}in / {summary['total_output_tokens']}out  |  "
          f"wall time: {summary['wall_seconds']:.1f}s")
    print()


def compare(path_a: Path, path_b: Path) -> None:
    a = json.loads(path_a.read_text())
    b = json.loads(path_b.read_text())

    results_a = {r["bug_id"]: r for r in a["results"]}
    results_b = {r["bug_id"]: r for r in b["results"]}
    all_ids = sorted(set(results_a) | set(results_b))

    label_a = a.get("run_id") or path_a.parent.name
    label_b = b.get("run_id") or path_b.parent.name

    col = {"bug_id": 28, "a": 8, "b": 8, "change": 7}
    header = (
        f"{'bug_id':<{col['bug_id']}}"
        f"{'A':<{col['a']}}"
        f"{'B':<{col['b']}}"
        f"{'change':<{col['change']}}"
    )
    divider = "-" * len(header)

    model_a = f" / {a['model']}" if a.get("model") else ""
    model_b = f" / {b['model']}" if b.get("model") else ""
    print(f"\nA: {label_a}  ({a['agent']}{model_a})")
    print(f"B: {label_b}  ({b['agent']}{model_b})")
    print(divider)
    print(header)
    print(divider)

    fixed = broke = 0
    for bug_id in all_ids:
        ra = results_a.get(bug_id)
        rb = results_b.get(bug_id)
        sa = ("OK" if ra["all_passed"] else "FAIL") if ra else "N/A"
        sb = ("OK" if rb["all_passed"] else "FAIL") if rb else "N/A"
        if sa == sb:
            change = "="
        elif sa == "FAIL" and sb == "OK":
            change = "fixed"
            fixed += 1
        elif sa == "OK" and sb == "FAIL":
            change = "broke"
            broke += 1
        else:
            change = "?"
        print(
            f"{bug_id:<{col['bug_id']}}"
            f"{sa:<{col['a']}}"
            f"{sb:<{col['b']}}"
            f"{change:<{col['change']}}"
        )

    print(divider)
    pa = a["pass_rate"] * 100
    pb = b["pass_rate"] * 100
    delta = pb - pa
    delta_str = f"+{delta:.1f}%" if delta >= 0 else f"{delta:.1f}%"
    print(f"A: {a['bugs_passed']}/{a['total_bugs']} ({pa:.1f}%)  "
          f"B: {b['bugs_passed']}/{b['total_bugs']} ({pb:.1f}%)  "
          f"delta: {delta_str}  fixed: {fixed}  broke: {broke}")
    print()


def list_runs(runs_path: Path = Path("results/runs.json")) -> None:
    if not runs_path.exists():
        print("No runs recorded yet. Run a batch first.")
        return
    entries = json.loads(runs_path.read_text())
    if not entries:
        print("No runs recorded yet.")
        return

    col = {"run_id": 42, "agent": 12, "model": 22, "pass_rate": 10, "passed": 8}
    header = (
        f"{'run_id':<{col['run_id']}}"
        f"{'agent':<{col['agent']}}"
        f"{'model':<{col['model']}}"
        f"{'pass_rate':<{col['pass_rate']}}"
        f"{'passed':<{col['passed']}}"
    )
    divider = "-" * len(header)

    print(f"\nBatch runs ({len(entries)} total):")
    print(divider)
    print(header)
    print(divider)
    for e in entries:
        pass_pct = f"{e['pass_rate'] * 100:.1f}%"
        passed = f"{e['bugs_passed']}/{e['total_bugs']}"
        print(
            f"{(e.get('run_id') or '?'):<{col['run_id']}}"
            f"{e.get('agent', '?'):<{col['agent']}}"
            f"{(e.get('model') or '-'):<{col['model']}}"
            f"{pass_pct:<{col['pass_rate']}}"
            f"{passed:<{col['passed']}}"
        )
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a report or compare batch runs.")
    parser.add_argument("summaries", nargs="*", type=Path,
                        help="Path(s) to summary.json: one for a report, two for a comparison")
    parser.add_argument("--list", action="store_true", help="List all recorded batch runs")
    args = parser.parse_args()

    if args.list:
        list_runs()
    elif len(args.summaries) == 2:
        compare(args.summaries[0], args.summaries[1])
    elif len(args.summaries) == 1:
        report(args.summaries[0])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
