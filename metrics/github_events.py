"""Fetch recent public events for a GitHub repository."""

from typing import Any, Optional

import requests

GITHUB_API = "https://api.github.com"
DEFAULT_TIMEOUT = 30


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
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    events: list[dict[str, Any]] = []
    for page in range(1, pages + 1):
        response = requests.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/events",
            headers=headers,
            params={"per_page": per_page, "page": page},
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        events.extend(batch)

    return events
