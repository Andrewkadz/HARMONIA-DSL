"""Print baseline and overlay metrics for a GitHub repository."""

from github_events import fetch_repo_events
from metrics_baseline import weekly_activity
from ri1_overlay import harmonic_coherence_index


def main() -> None:
    owner = "Andrewkadz"
    repo = "HARMONIA-DSL"

    events = fetch_repo_events(owner, repo, token=None)
    print(f"Fetched {len(events)} events for {owner}/{repo}\n")

    print("Weekly activity:")
    counts = weekly_activity(events)
    if counts.empty:
        print("  (no events)")
    for week, count in counts.items():
        print(f"  {week.date()}: {count}")

    print(f"\nHarmonic coherence index: {harmonic_coherence_index(events):.4f}")


if __name__ == "__main__":
    main()
