"""Assemble the full metrics payload for a repository."""

from datetime import datetime, timezone
from typing import Any, Optional

from github_events import fetch_issues, fetch_pull_requests, fetch_repo_events
from levers import candidate_levers, recommended_lever
from metrics_baseline import activity_to_dict
from ri1_overlay import coherence_to_dict, harmonic_coherence_index


def build_report(
    owner: str,
    repo: str,
    token: Optional[str] = None,
    pages: int = 1,
    include_levers: bool = True,
) -> dict[str, Any]:
    """Fetch activity for ``owner/repo`` and return the full metrics payload.

    ``include_levers`` controls whether the pull request and issue endpoints
    are queried as well; disabling it keeps the run to a single API call.
    """
    events = fetch_repo_events(owner, repo, token=token, pages=pages)
    pulls = fetch_pull_requests(owner, repo, token=token) if include_levers else []
    issues = fetch_issues(owner, repo, token=token) if include_levers else []

    candidates = candidate_levers(events, pulls, issues)
    return assemble_report(owner, repo, events, candidates)


def assemble_report(
    owner: str,
    repo: str,
    events: list[dict[str, Any]],
    candidates: Optional[list[Any]] = None,
) -> dict[str, Any]:
    """Build the payload from already-fetched data (no network access)."""
    candidates = candidates or []
    return {
        "owner": owner,
        "repo": repo,
        "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        **activity_to_dict(events),
        **coherence_to_dict(
            harmonic_coherence_index(events),
            recommended_lever(candidates),
            candidates,
        ),
    }
