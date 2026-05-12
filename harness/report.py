import argparse
import json
from pathlib import Path


def report(summary_path: Path) -> None:
    summary = json.loads(summary_path.read_text())
    results = summary["results"]

    col_widths = {"bug_id": 24, "status": 8, "tests": 10, "latency": 10, "tokens_in": 10, "tokens_out": 11}
    header = (
        f"{'bug_id':<{col_widths['bug_id']}}"
        f"{'status':<{col_widths['status']}}"
        f"{'tests':<{col_widths['tests']}}"
        f"{'latency':<{col_widths['latency']}}"
        f"{'tokens_in':<{col_widths['tokens_in']}}"
        f"{'tokens_out':<{col_widths['tokens_out']}}"
    )
    divider = "-" * len(header)

    print(f"\nAgent: {summary['agent']}")
    print(divider)
    print(header)
    print(divider)

    for r in results:
        status = "OK" if r["all_passed"] else "FAIL"
        tests = f"{r['passed']}/{r['total']}"
        latency = f"{r['latency_seconds']:.2f}s"
        tokens_in = str(r["input_tokens"]) if r["input_tokens"] is not None else "-"
        tokens_out = str(r["output_tokens"]) if r["output_tokens"] is not None else "-"
        print(
            f"{r['bug_id']:<{col_widths['bug_id']}}"
            f"{status:<{col_widths['status']}}"
            f"{tests:<{col_widths['tests']}}"
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a report from a batch summary.")
    parser.add_argument("summary", type=Path, help="Path to summary.json")
    args = parser.parse_args()

    report(args.summary)


if __name__ == "__main__":
    main()
