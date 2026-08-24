"""Append-only, timestamped store of metric runs.

Each run is one JSON object per line so the file can be tailed, diffed, or read
into pandas without a database. Point ``METRICS_HISTORY_PATH`` elsewhere to keep
history outside the repository.
"""

import json
import os
from pathlib import Path
from typing import Any, Optional

DEFAULT_HISTORY_PATH = Path(__file__).resolve().parent / "history.jsonl"


def history_path() -> Path:
    return Path(os.environ.get("METRICS_HISTORY_PATH", DEFAULT_HISTORY_PATH))


def scalar_snapshot(report: dict[str, Any]) -> dict[str, Any]:
    """Reduce a report to the scalars worth tracking over time."""
    lever = report["ri1"].get("recommended_lever")
    return {
        "collected_at": report["collected_at"],
        "owner": report["owner"],
        "repo": report["repo"],
        "event_count": report["baseline"]["event_count"],
        "harmonic_coherence_index": report["ri1"]["harmonic_coherence_index"],
        "recommended_lever": lever["name"] if lever else None,
        "recommended_lever_value": lever["current_value"] if lever else None,
    }


def record_run(report: dict[str, Any], path: Optional[Path] = None) -> Path:
    """Append ``report``'s scalars to the history file and return its path."""
    target = path or history_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(scalar_snapshot(report)) + "\n")
    return target


def load_history(
    owner: Optional[str] = None,
    repo: Optional[str] = None,
    path: Optional[Path] = None,
) -> list[dict[str, Any]]:
    """Return recorded runs, optionally filtered to one repository."""
    target = path or history_path()
    if not target.exists():
        return []

    runs = []
    for line in target.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        run = json.loads(line)
        if owner and run.get("owner") != owner:
            continue
        if repo and run.get("repo") != repo:
            continue
        runs.append(run)

    return runs
