import json
from pathlib import Path
from typing import Any

from history import load_history, record_run, scalar_snapshot
from levers import candidate_levers
from oscal import to_assessment_results
from prometheus import render_prometheus
from report import assemble_report

EVENTS: list[dict[str, Any]] = [
    {"type": "PushEvent", "created_at": "2024-01-01T10:00:00Z"},
    {"type": "PullRequestEvent", "created_at": "2024-01-02T10:00:00Z"},
    {"type": "IssueCommentEvent", "created_at": "2024-01-03T10:00:00Z"},
]


def build() -> dict[str, Any]:
    return assemble_report("acme", "widget", EVENTS, candidate_levers(EVENTS))


def test_report_shape() -> None:
    report = build()

    assert report["owner"] == "acme"
    assert report["baseline"]["event_count"] == 3
    assert report["ri1"]["harmonic_coherence_index"] == 2.0
    # discussion_density is 0.5, above its 0.2 target, so nothing to recommend.
    assert report["ri1"]["recommended_lever"] is None
    assert [c["name"] for c in report["ri1"]["candidate_levers"]] == [
        "discussion_density"
    ]


def test_render_prometheus() -> None:
    text = render_prometheus(build())

    assert "# TYPE ri1_event_count gauge" in text
    assert 'ri1_event_count{owner="acme",repo="widget"} 3' in text
    assert 'ri1_events_by_type{owner="acme",repo="widget",type="PushEvent"} 1' in text
    assert 'ri1_weekly_events{owner="acme",repo="widget",week="2024-01-07"} 3' in text
    assert 'ri1_harmonic_coherence_index{owner="acme",repo="widget"} 2.0' in text
    assert 'ri1_recommended_lever{owner="acme",repo="widget",lever="discussion_density"} 0' in text
    assert text.endswith("\n")


def test_prometheus_omits_undefined_coherence() -> None:
    report = assemble_report("acme", "widget", [EVENTS[0]], [])

    assert "ri1_harmonic_coherence_index" not in render_prometheus(report).split("# ")[-1]


def test_assessment_results_is_deterministic() -> None:
    report = build()
    first = to_assessment_results(report)
    second = to_assessment_results(report)

    assert first == second
    results = first["assessment-results"]
    assert results["metadata"]["oscal-version"] == "1.1.2"
    assert [o["title"] for o in results["results"][0]["observations"]] == [
        "event_count",
        "weekly_activity",
        "harmonic_coherence_index",
    ]
    assert results["results"][0]["findings"] == []
    assert first["ri1-payload"] == report


def test_history_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "history.jsonl"
    report = build()

    record_run(report, path)
    record_run({**report, "owner": "other"}, path)

    assert load_history("acme", "widget", path) == [scalar_snapshot(report)]
    assert len(load_history(path=path)) == 2
    assert json.loads(path.read_text().splitlines()[0])["event_count"] == 3


def test_load_history_missing_file(tmp_path: Path) -> None:
    assert load_history(path=tmp_path / "nope.jsonl") == []
