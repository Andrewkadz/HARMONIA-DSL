"""Print baseline and overlay metrics for a GitHub repository."""

import argparse
import json
import os

from github_events import fetch_repo_events
from metrics_baseline import activity_to_dict, event_type_counts, weekly_activity
from ri1_overlay import coherence_to_dict, harmonic_coherence_index

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
        "--json",
        action="store_true",
        help="emit machine-readable JSON instead of formatted text",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN")

    events = fetch_repo_events(args.owner, args.repo, token=token)
    counts = weekly_activity(events)
    coherence = harmonic_coherence_index(events)

    if args.json:
        print(json.dumps({**activity_to_dict(events), **coherence_to_dict(coherence)}))
        return

    print(f"Fetched {len(events)} events for {args.owner}/{args.repo}\n")

    print("Baseline - events by type:")
    for event_type, count in sorted(event_type_counts(events).items()):
        print(f"  {event_type}: {count}")

    print("\nBaseline - weekly activity:")
    if counts.empty:
        print("  (no events)")
    for week, count in counts.items():
        print(f"  {week.date()}: {count}")

    print(f"\nRI1 - harmonic coherence index: {coherence:.4f}")


if __name__ == "__main__":
    main()
