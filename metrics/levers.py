"""Candidate organisational levers derived from GitHub activity.

Each lever is a single tunable parameter with a target value. ``severity`` is
the ratio between the observed value and its target, expressed so that ``1.0``
means "exactly on target" and anything above ``1.0`` means "out of band"; the
lever with the highest severity is the one worth acting on first.
"""

import statistics
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

REVIEW_THROUGHPUT_TARGET_HOURS = 48.0
ISSUE_CLOSURE_TARGET_RATIO = 0.5
DISCUSSION_DENSITY_TARGET_RATIO = 0.2

CODE_EVENT_TYPES = frozenset({"PushEvent", "PullRequestEvent"})
DISCUSSION_EVENT_TYPES = frozenset(
    {"IssueCommentEvent", "PullRequestReviewCommentEvent", "PullRequestReviewEvent"}
)


@dataclass(frozen=True)
class Lever:
    """A single tunable parameter, its current value, and its target."""

    name: str
    description: str
    current_value: float
    target_value: float
    unit: str
    severity: float
    sample_size: int
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "current_value": round(self.current_value, 4),
            "target_value": self.target_value,
            "unit": self.unit,
            "severity": round(self.severity, 4),
            "sample_size": self.sample_size,
            **self.extras,
        }


def _parse(timestamp: Optional[str]) -> Optional[datetime]:
    if not timestamp:
        return None
    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None


def review_throughput(pull_requests: list[dict[str, Any]]) -> Optional[Lever]:
    """Median hours from pull request opened to closed."""
    durations = []
    for pull in pull_requests:
        opened = _parse(pull.get("created_at"))
        closed = _parse(pull.get("closed_at"))
        if opened and closed and closed >= opened:
            durations.append((closed - opened).total_seconds() / 3600)

    if not durations:
        return None

    median_hours = statistics.median(durations)
    return Lever(
        name="review_throughput",
        description=(
            "Reduce median PR review time below "
            f"{REVIEW_THROUGHPUT_TARGET_HOURS:.0f}h"
        ),
        current_value=median_hours,
        target_value=REVIEW_THROUGHPUT_TARGET_HOURS,
        unit="hours",
        severity=median_hours / REVIEW_THROUGHPUT_TARGET_HOURS,
        sample_size=len(durations),
    )


def issue_closure_ratio(issues: list[dict[str, Any]]) -> Optional[Lever]:
    """Share of recent issues that are closed."""
    if not issues:
        return None

    closed = sum(1 for issue in issues if issue.get("state") == "closed")
    ratio = closed / len(issues)
    # A ratio of zero is maximally out of band; clamp so severity stays finite.
    severity = ISSUE_CLOSURE_TARGET_RATIO / max(ratio, 1 / (2 * len(issues)))
    return Lever(
        name="issue_closure_ratio",
        description=(
            "Raise the share of recent issues that get closed above "
            f"{ISSUE_CLOSURE_TARGET_RATIO:.0%}"
        ),
        current_value=ratio,
        target_value=ISSUE_CLOSURE_TARGET_RATIO,
        unit="ratio",
        severity=severity,
        sample_size=len(issues),
        extras={"closed_issues": closed, "open_issues": len(issues) - closed},
    )


def discussion_density(events: list[dict[str, Any]]) -> Optional[Lever]:
    """Discussion events per code event.

    Unlike ``harmonic_coherence_index`` this counts reviews and review comments
    as discussion, so review-centric projects are not misread as silent.
    """
    code = sum(1 for e in events if e.get("type") in CODE_EVENT_TYPES)
    discussion = sum(1 for e in events if e.get("type") in DISCUSSION_EVENT_TYPES)
    if not code:
        return None

    ratio = discussion / code
    severity = DISCUSSION_DENSITY_TARGET_RATIO / max(ratio, 1 / (2 * code))
    return Lever(
        name="discussion_density",
        description=(
            "Raise recorded review/discussion per code event above "
            f"{DISCUSSION_DENSITY_TARGET_RATIO:.1f}"
        ),
        current_value=ratio,
        target_value=DISCUSSION_DENSITY_TARGET_RATIO,
        unit="ratio",
        severity=severity,
        sample_size=code + discussion,
        extras={"code_events": code, "discussion_events": discussion},
    )


def candidate_levers(
    events: list[dict[str, Any]],
    pull_requests: Optional[list[dict[str, Any]]] = None,
    issues: Optional[list[dict[str, Any]]] = None,
) -> list[Lever]:
    """Return every lever that could be computed from the supplied data."""
    computed = [
        review_throughput(pull_requests or []),
        issue_closure_ratio(issues or []),
        discussion_density(events),
    ]
    return [lever for lever in computed if lever is not None]


def recommended_lever(levers: list[Lever]) -> Optional[Lever]:
    """Return the single most out-of-band lever, or ``None`` if all are on target."""
    if not levers:
        return None

    worst = max(levers, key=lambda lever: lever.severity)
    return worst if worst.severity > 1.0 else None
