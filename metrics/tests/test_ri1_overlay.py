import math
from typing import Any

from levers import Lever
from ri1_overlay import COHERENCE_NOTES, coherence_to_dict, harmonic_coherence_index
from version import METRICS_VERSION


def event(event_type: str) -> dict[str, Any]:
    return {"type": event_type, "created_at": "2024-01-01T10:00:00Z"}


def test_no_events() -> None:
    assert harmonic_coherence_index([]) == 0.0


def test_only_code_events_is_infinite() -> None:
    events = [event("PushEvent"), event("PullRequestEvent")]

    assert math.isinf(harmonic_coherence_index(events))


def test_only_discussion_events_is_zero() -> None:
    assert harmonic_coherence_index([event("IssueCommentEvent")]) == 0.0


def test_mixed_events_is_ratio() -> None:
    events = [
        event("PushEvent"),
        event("PullRequestEvent"),
        event("PullRequestEvent"),
        event("IssueCommentEvent"),
        event("WatchEvent"),  # neither code nor discussion
    ]

    assert harmonic_coherence_index(events) == 3.0


def test_coherence_to_dict_maps_infinity_to_null() -> None:
    assert coherence_to_dict(math.inf) == {
        "ri1": {
            "version": METRICS_VERSION,
            "harmonic_coherence_index": None,
            "notes": COHERENCE_NOTES,
            "recommended_lever": None,
            "candidate_levers": [],
        }
    }
    assert coherence_to_dict(2.0)["ri1"]["harmonic_coherence_index"] == 2.0


def test_coherence_to_dict_includes_levers() -> None:
    lever = Lever(
        name="review_throughput",
        description="Reduce median PR review time below 48h",
        current_value=92.0,
        target_value=48.0,
        unit="hours",
        severity=92.0 / 48.0,
        sample_size=7,
    )

    block = coherence_to_dict(2.0, lever, [lever])["ri1"]

    assert block["recommended_lever"]["name"] == "review_throughput"
    assert block["recommended_lever"]["current_value"] == 92.0
    assert [c["name"] for c in block["candidate_levers"]] == ["review_throughput"]
