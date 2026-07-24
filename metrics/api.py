"""HTTP API exposing the RI1 metrics for any GitHub repository."""

import os
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from requests import HTTPError

from github_events import fetch_repo_events
from metrics_baseline import activity_to_dict
from ri1_overlay import coherence_to_dict, harmonic_coherence_index
from version import METRICS_VERSION

app = FastAPI(title="HARMONIA-DSL metrics", version=METRICS_VERSION)


@app.get("/metrics/{owner}/{repo}")
def repo_metrics(owner: str, repo: str, pages: int = 1) -> dict[str, Any]:
    token: Optional[str] = os.environ.get("GITHUB_TOKEN")
    try:
        events = fetch_repo_events(owner, repo, token=token, pages=pages)
    except HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else 502
        raise HTTPException(status_code=status, detail=str(exc)) from exc

    return {
        "owner": owner,
        "repo": repo,
        **activity_to_dict(events),
        **coherence_to_dict(harmonic_coherence_index(events)),
    }
