"""Baseline activity metrics derived from GitHub events.

These are conventional, CHAOSS-style counts: they make no claims beyond what
the GitHub events feed reports.
"""

import json
from collections import Counter
from typing import Any

import pandas as pd


def weekly_activity(events: list[dict[str, Any]]) -> pd.Series:
    """Return the number of events per calendar week."""
    if not events:
        return pd.Series(dtype="int64")

    frame = pd.DataFrame(events)
    frame["created_at"] = pd.to_datetime(frame["created_at"], utc=True, errors="coerce")
    frame = frame.dropna(subset=["created_at"])
    if frame.empty:
        return pd.Series(dtype="int64")

    return frame.set_index("created_at").resample("W").size()


def event_type_counts(events: list[dict[str, Any]]) -> dict[str, int]:
    """Return the number of events per GitHub event type."""
    return dict(Counter(event.get("type", "UnknownEvent") for event in events))


def activity_to_dict(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Return the JSON-serialisable ``baseline`` block for ``events``."""
    return {
        "baseline": {
            "event_count": len(events),
            "event_type_counts": event_type_counts(events),
            "weekly_activity": [
                {"week": week.strftime("%Y-%m-%d"), "events": int(count)}
                for week, count in weekly_activity(events).items()
            ],
        }
    }


def activity_to_json(events: list[dict[str, Any]]) -> str:
    """Return the ``baseline`` block as a JSON string."""
    return json.dumps(activity_to_dict(events))
