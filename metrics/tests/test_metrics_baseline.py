from typing import Any

from metrics_baseline import (
    activity_to_dict,
    event_type_counts,
    weekly_activity,
)


def event(created_at: str, event_type: str = "PushEvent") -> dict[str, Any]:
    return {"type": event_type, "created_at": created_at}


def test_weekly_activity_groups_by_week() -> None:
    events = [
        event("2024-01-01T10:00:00Z"),  # week ending 2024-01-07
        event("2024-01-05T10:00:00Z"),  # week ending 2024-01-07
        event("2024-01-15T10:00:00Z"),  # week ending 2024-01-21
    ]

    counts = weekly_activity(events)

    assert [week.strftime("%Y-%m-%d") for week in counts.index] == [
        "2024-01-07",
        "2024-01-14",
        "2024-01-21",
    ]
    assert list(counts) == [2, 0, 1]


def test_weekly_activity_handles_empty_and_unparsable_input() -> None:
    assert weekly_activity([]).empty
    assert weekly_activity([event("not-a-date")]).empty


def test_event_type_counts() -> None:
    events = [
        event("2024-01-01T10:00:00Z", "PushEvent"),
        event("2024-01-02T10:00:00Z", "PushEvent"),
        event("2024-01-03T10:00:00Z", "IssueCommentEvent"),
        {"created_at": "2024-01-04T10:00:00Z"},
    ]

    assert event_type_counts(events) == {
        "PushEvent": 2,
        "IssueCommentEvent": 1,
        "UnknownEvent": 1,
    }


def test_activity_to_dict_shape() -> None:
    payload = activity_to_dict([event("2024-01-01T10:00:00Z")])

    assert payload == {
        "baseline": {
            "event_count": 1,
            "event_type_counts": {"PushEvent": 1},
            "weekly_activity": [{"week": "2024-01-07", "events": 1}],
        }
    }
