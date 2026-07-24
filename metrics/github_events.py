"""Fetch recent public activity for a GitHub repository."""

from typing import Any, Optional

import requests

GITHUB_API = "https://api.github.com"
DEFAULT_TIMEOUT = 30


def _headers(token: Optional[str]) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _fetch_paginated(
    path: str,
    token: Optional[str],
    params: dict[str, Any],
    per_page: int,
    pages: int,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for page in range(1, pages + 1):
        response = requests.get(
            f"{GITHUB_API}{path}",
            headers=_headers(token),
            params={**params, "per_page": per_page, "page": page},
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        items.extend(batch)

    return items


def fetch_repo_events(
    owner: str,
    repo: str,
    token: Optional[str] = None,
    per_page: int = 100,
    pages: int = 1,
) -> list[dict[str, Any]]:
    """Return recent events for ``owner/repo`` via the GitHub REST events API.

    ``token`` is optional; supplying one raises the rate limit and allows
    access to private repositories.
    """
    return _fetch_paginated(
        f"/repos/{owner}/{repo}/events", token, {}, per_page, pages
    )


def fetch_pull_requests(
    owner: str,
    repo: str,
    token: Optional[str] = None,
    per_page: int = 100,
    pages: int = 1,
) -> list[dict[str, Any]]:
    """Return the most recently updated closed pull requests for ``owner/repo``."""
    return _fetch_paginated(
        f"/repos/{owner}/{repo}/pulls",
        token,
        {"state": "closed", "sort": "updated", "direction": "desc"},
        per_page,
        pages,
    )


def fetch_issues(
    owner: str,
    repo: str,
    token: Optional[str] = None,
    per_page: int = 100,
    pages: int = 1,
) -> list[dict[str, Any]]:
    """Return recent issues for ``owner/repo``.

    The GitHub issues endpoint also returns pull requests; those carry a
    ``pull_request`` key and are filtered out here.
    """
    issues = _fetch_paginated(
        f"/repos/{owner}/{repo}/issues",
        token,
        {"state": "all", "sort": "updated", "direction": "desc"},
        per_page,
        pages,
    )
    return [issue for issue in issues if "pull_request" not in issue]
