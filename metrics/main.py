"""Print baseline and overlay metrics for a GitHub repository."""

import argparse
import json
import os

from history import record_run
from oscal import to_assessment_results
from prometheus import render_prometheus
from report import build_report

DEFAULT_OWNER = "Andrewkadz"
DEFAULT_REPO = "HARMONIA-DSL"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--owner",
        default=os.environ.get("METRICS_OWNER", DEFAULT_OWNER),
        help="repository owner (env: METRICS_OWNER)",
    )
    parser.add_argument(
        "--repo",
        default=os.environ.get("METRICS_REPO", DEFAULT_REPO),
        help="repository name (env: METRICS_REPO)",
    )
    parser.add_argument(
        "--pages", type=int, default=1, help="pages of events to fetch (100 each)"
    )
    parser.add_argument(
        "--no-levers",
        action="store_true",
        help="skip the pull request and issue calls used for lever selection",
    )
    parser.add_argument(
        "--no-record",
        action="store_true",
        help="do not append this run to the history file",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json", "prometheus", "oscal"),
        default="text",
        help="output format (default: text)",
    )
    parser.add_argument(
        "--json",
        dest="format",
        action="store_const",
        const="json",
        help="shorthand for --format json",
    )
    return parser.parse_args()


def print_text(report: dict) -> None:
    baseline = report["baseline"]
    ri1 = report["ri1"]

    print(f"Fetched {baseline['event_count']} events for {report['owner']}/{report['repo']}\n")

    print("Baseline - events by type:")
    for event_type, count in sorted(baseline["event_type_counts"].items()):
        print(f"  {event_type}: {count}")

    print("\nBaseline - weekly activity:")
    if not baseline["weekly_activity"]:
        print("  (no events)")
    for bucket in baseline["weekly_activity"]:
        print(f"  {bucket['week']}: {bucket['events']}")

    coherence = ri1["harmonic_coherence_index"]
    shown = "undefined (no discussion events)" if coherence is None else f"{coherence:.4f}"
    print(f"\nRI1 - harmonic coherence index: {shown}")

    print("RI1 - recommended lever:")
    lever = ri1["recommended_lever"]
    if lever is None:
        print("  (every candidate lever is within its target band)")
    else:
        print(f"  {lever['name']}: {lever['description']}")
        print(
            f"  current {lever['current_value']} {lever['unit']} "
            f"vs target {lever['target_value']} {lever['unit']} "
            f"(severity {lever['severity']}, n={lever['sample_size']})"
        )


def main() -> None:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN")

    report = build_report(
        args.owner,
        args.repo,
        token=token,
        pages=args.pages,
        include_levers=not args.no_levers,
    )
    if not args.no_record:
        record_run(report)

    if args.format == "json":
        print(json.dumps(report))
    elif args.format == "prometheus":
        print(render_prometheus(report), end="")
    elif args.format == "oscal":
        print(json.dumps(to_assessment_results(report)))
    else:
        print_text(report)


if __name__ == "__main__":
    main()
