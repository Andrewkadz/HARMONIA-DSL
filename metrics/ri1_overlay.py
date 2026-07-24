"""Placeholder RI-1 overlay metrics."""

import json
import math
from typing import Any, Optional

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


def coherence_to_dict(coherence: float) -> dict[str, Optional[float]]:
    """Return the coherence index as a JSON-serialisable dict.

    ``inf`` is mapped to ``None`` since JSON has no infinity literal.
    """
    return {
        "harmonic_coherence_index": None if math.isinf(coherence) else coherence
    }


def coherence_to_json(coherence: float) -> str:
    """Return the coherence index as a JSON string."""
    return json.dumps(coherence_to_dict(coherence))
