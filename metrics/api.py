"""HTTP API exposing the RI1 metrics for any GitHub repository."""

import os
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Response
from requests import HTTPError

from history import load_history, record_run
from oscal import to_assessment_results
from prometheus import CONTENT_TYPE, render_prometheus
from report import build_report
from version import METRICS_VERSION

app = FastAPI(title="HARMONIA-DSL metrics", version=METRICS_VERSION)


def _report(owner: str, repo: str, pages: int, levers: bool) -> dict[str, Any]:
    token: Optional[str] = os.environ.get("GITHUB_TOKEN")
    try:
        report = build_report(
            owner, repo, token=token, pages=pages, include_levers=levers
        )
    except HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else 502
        raise HTTPException(status_code=status, detail=str(exc)) from exc

    record_run(report)
    return report


@app.get("/metrics/{owner}/{repo}")
def repo_metrics(
    owner: str, repo: str, pages: int = 1, levers: bool = True
) -> dict[str, Any]:
    """Full JSON payload: baseline metrics plus the RI1 overlay."""
    return _report(owner, repo, pages, levers)


@app.get("/metrics", response_class=Response)
def prometheus_metrics(
    owner: str, repo: str, pages: int = 1, levers: bool = True
) -> Response:
    """Prometheus exposition format for a single repository target."""
    report = _report(owner, repo, pages, levers)
    return Response(content=render_prometheus(report), media_type=CONTENT_TYPE)


@app.get("/assessment/{owner}/{repo}")
def repo_assessment(
    owner: str, repo: str, pages: int = 1, levers: bool = True
) -> dict[str, Any]:
    """The same measurements shaped as an OSCAL-style assessment-results object."""
    return to_assessment_results(_report(owner, repo, pages, levers))


@app.get("/history/{owner}/{repo}")
def repo_history(owner: str, repo: str) -> dict[str, Any]:
    """Timestamped scalars from previous runs, oldest first."""
    return {"owner": owner, "repo": repo, "runs": load_history(owner, repo)}
