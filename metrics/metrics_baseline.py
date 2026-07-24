"""Baseline activity metrics derived from GitHub events."""

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
