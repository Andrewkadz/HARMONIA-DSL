from typing import Any

from levers import (
    Lever,
    candidate_levers,
    discussion_density,
    issue_closure_ratio,
    recommended_lever,
    review_throughput,
)


def pull(created: str, closed: str) -> dict[str, Any]:
    return {"created_at": created, "closed_at": closed}


def lever(name: str, severity: float) -> Lever:
    return Lever(
        name=name,
        description="",
        current_value=1.0,
        target_value=1.0,
        unit="ratio",
        severity=severity,
        sample_size=1,
    )


def test_review_throughput_is_median_hours() -> None:
    pulls = [
        pull("2024-01-01T00:00:00Z", "2024-01-01T12:00:00Z"),  # 12h
        pull("2024-01-01T00:00:00Z", "2024-01-03T00:00:00Z"),  # 48h
        pull("2024-01-01T00:00:00Z", "2024-01-05T00:00:00Z"),  # 96h
        {"created_at": "2024-01-01T00:00:00Z", "closed_at": None},  # still open
    ]

    result = review_throughput(pulls)

    assert result is not None
    assert result.current_value == 48.0
    assert result.severity == 1.0
    assert result.sample_size == 3


def test_review_throughput_without_closed_pulls() -> None:
    assert review_throughput([]) is None
    assert review_throughput([{"created_at": "2024-01-01T00:00:00Z"}]) is None


def test_issue_closure_ratio() -> None:
    issues = [{"state": "closed"}, {"state": "closed"}, {"state": "open"}]

    result = issue_closure_ratio(issues)

    assert result is not None
    assert round(result.current_value, 4) == 0.6667
    assert result.severity < 1.0  # above target, so not a lever worth pulling
    assert result.extras == {"closed_issues": 2, "open_issues": 1}


def test_issue_closure_ratio_with_no_closures_stays_finite() -> None:
    result = issue_closure_ratio([{"state": "open"}, {"state": "open"}])

    assert result is not None
    assert result.current_value == 0.0
    assert result.severity == 2.0  # 0.5 / (1 / (2 * 2))


def test_discussion_density_counts_reviews_as_discussion() -> None:
    events = [
        {"type": "PushEvent"},
        {"type": "PullRequestEvent"},
        {"type": "PullRequestReviewEvent"},
        {"type": "WatchEvent"},
    ]

    result = discussion_density(events)

    assert result is not None
    assert result.current_value == 0.5
    assert result.extras == {"code_events": 2, "discussion_events": 1}


def test_discussion_density_without_code_events() -> None:
    assert discussion_density([{"type": "WatchEvent"}]) is None


def test_candidate_levers_skips_uncomputable_ones() -> None:
    names = [
        candidate.name
        for candidate in candidate_levers([{"type": "PushEvent"}], [], [])
    ]

    assert names == ["discussion_density"]


def test_recommended_lever_picks_worst_out_of_band() -> None:
    worst = lever("review_throughput", 3.0)

    assert recommended_lever([lever("a", 1.5), worst]) is worst


def test_recommended_lever_is_none_when_everything_on_target() -> None:
    assert recommended_lever([lever("a", 0.9), lever("b", 1.0)]) is None
    assert recommended_lever([]) is None
