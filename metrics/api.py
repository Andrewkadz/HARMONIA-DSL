"""HTTP API exposing the RI1 metrics for any GitHub repository."""

import os
from collections import Counter
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from requests import HTTPError

from github_events import fetch_repo_events
from metrics_baseline import activity_to_dict, weekly_activity
from ri1_overlay import coherence_to_dict, harmonic_coherence_index

app = FastAPI(title="HARMONIA-DSL metrics", version="0.1.0")


def event_type_counts(events: list[dict[str, Any]]) -> dict[str, int]:
    """Return a CHAOSS-style count of events per event type."""
    return dict(Counter(event.get("type", "UnknownEvent") for event in events))


@app.get("/metrics/{owner}/{repo}")
def repo_metrics(owner: str, repo: str, pages: int = 1) -> dict[str, Any]:
    token: Optional[str] = os.environ.get("GITHUB_TOKEN")
    try:
        events = fetch_repo_events(owner, repo, token=token, pages=pages)
    except HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else 502
        raise HTTPException(status_code=status, detail=str(exc)) from exc

    coherence = harmonic_coherence_index(events)
    return {
        "owner": owner,
        "repo": repo,
        "event_count": len(events),
        "event_type_counts": event_type_counts(events),
        **activity_to_dict(weekly_activity(events)),
        **coherence_to_dict(coherence),
    }
