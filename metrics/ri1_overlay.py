"""RI1 overlay metrics.

These are experimental, RI1-specific interpretations layered on top of the
baseline counts; they are versioned separately so they can be evaluated (or
rejected) independently of the baseline metrics.
"""

import json
import math
from typing import Any, Optional

from version import METRICS_VERSION

CODE_EVENT_TYPES = frozenset({"PushEvent", "PullRequestEvent"})
SOCIAL_EVENT_TYPES = frozenset({"IssueCommentEvent"})

COHERENCE_NOTES = (
    "ratio of code events (Push/PullRequest) to discussion events (IssueComment)"
)


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


def coherence_to_dict(coherence: float) -> dict[str, Any]:
    """Return the JSON-serialisable ``ri1`` block for ``coherence``.

    ``inf`` is mapped to ``None`` since JSON has no infinity literal.
    """
    value: Optional[float] = None if math.isinf(coherence) else coherence
    return {
        "ri1": {
            "version": METRICS_VERSION,
            "harmonic_coherence_index": value,
            "notes": COHERENCE_NOTES,
        }
    }


def coherence_to_json(coherence: float) -> str:
    """Return the ``ri1`` block as a JSON string."""
    return json.dumps(coherence_to_dict(coherence))
