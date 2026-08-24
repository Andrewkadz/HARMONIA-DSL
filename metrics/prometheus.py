"""Render a metrics report in the Prometheus text exposition format."""

from typing import Any

CONTENT_TYPE = "text/plain; version=0.0.4; charset=utf-8"

_HEADERS = [
    ("ri1_event_count", "gauge", "Number of GitHub events in the fetched window."),
    ("ri1_events_by_type", "gauge", "GitHub events in the window, by event type."),
    ("ri1_weekly_events", "gauge", "GitHub events per calendar week (week-ending)."),
    (
        "ri1_harmonic_coherence_index",
        "gauge",
        "Code events per discussion event; omitted when undefined.",
    ),
    ("ri1_lever_value", "gauge", "Current value of a candidate lever."),
    (
        "ri1_lever_severity",
        "gauge",
        "Lever value relative to its target; >1 means out of band.",
    ),
    (
        "ri1_recommended_lever",
        "gauge",
        "1 for the lever recommended for action, 0 for the others.",
    ),
]


def _escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _line(name: str, labels: dict[str, str], value: float) -> str:
    rendered = ",".join(f'{key}="{_escape(val)}"' for key, val in labels.items())
    return f"{name}{{{rendered}}} {value}"


def render_prometheus(report: dict[str, Any]) -> str:
    """Return ``report`` as Prometheus exposition text."""
    base = {"owner": report["owner"], "repo": report["repo"]}
    baseline = report["baseline"]
    ri1 = report["ri1"]

    lines = []
    for name, kind, help_text in _HEADERS:
        lines.append(f"# HELP {name} {help_text}")
        lines.append(f"# TYPE {name} {kind}")

    lines.append(_line("ri1_event_count", base, baseline["event_count"]))
    for event_type, count in sorted(baseline["event_type_counts"].items()):
        lines.append(_line("ri1_events_by_type", {**base, "type": event_type}, count))
    for bucket in baseline["weekly_activity"]:
        lines.append(
            _line("ri1_weekly_events", {**base, "week": bucket["week"]}, bucket["events"])
        )

    coherence = ri1["harmonic_coherence_index"]
    if coherence is not None:
        lines.append(_line("ri1_harmonic_coherence_index", base, coherence))

    recommended = (ri1.get("recommended_lever") or {}).get("name")
    for lever in ri1.get("candidate_levers", []):
        labels = {**base, "lever": lever["name"]}
        lines.append(_line("ri1_lever_value", labels, lever["current_value"]))
        lines.append(_line("ri1_lever_severity", labels, lever["severity"]))
        lines.append(
            _line("ri1_recommended_lever", labels, int(lever["name"] == recommended))
        )

    return "\n".join(lines) + "\n"
