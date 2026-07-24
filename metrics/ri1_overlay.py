"""Placeholder RI-1 overlay metrics."""

import math
from typing import Any

CODE_EVENT_TYPES = frozenset({"PushEvent", "PullRequestEvent"})
SOCIAL_EVENT_TYPES = frozenset({"IssueCommentEvent"})


def harmonic_coherence_index(events: list[dict[str, Any]]) -> float:
    """Ratio of code events to discussion events.

    Returns ``0.0`` when there are no code events and ``inf`` when there are
    code events but no discussion events.
    """
    code_events = [e for e in events if e.get("type") in CODE_EVENT_TYPES]
    social_events = [e for e in events if e.get("type") in SOCIAL_EVENT_TYPES]

    if not social_events:
        return math.inf if code_events else 0.0

    return len(code_events) / len(social_events)
