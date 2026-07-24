# metrics

Compute activity and a first RI1 coherence metric for HARMONIA-DSL using GitHub events.

Everything here is deterministic: it reads the public GitHub REST events API
(`/repos/{owner}/{repo}/events`) and derives numbers from it. No LLM calls.

Metrics are split into two groups, and the JSON payloads keep them separate so
each can be judged on its own terms:

- **baseline** — conventional, CHAOSS-style counts that make no claims beyond
  what the events feed reports.
- **ri1** — experimental RI1 overlays, versioned via `METRICS_VERSION` in
  `version.py` so a change in the formula is visible in the output.

## Install

```bash
pip install -r metrics/requirements.txt
```

## Run the CLI

```bash
cd metrics
python main.py
```

Point it at another repository with flags or environment variables:

```bash
python main.py --owner Andrewkadz --repo RI1-HYBRID-ENGINE
METRICS_OWNER=Andrewkadz METRICS_REPO=RI1-HYBRID-ENGINE python main.py
```

Add `--json` for machine-readable output:

```bash
python main.py --repo RI1-HYBRID-ENGINE --json
```

Set `GITHUB_TOKEN` to raise the API rate limit (60 requests/hour when
unauthenticated) and to read private repositories.

## HTTP API

```bash
cd metrics
uvicorn api:app --reload --port 8000
```

`GET http://localhost:8000/metrics/{owner}/{repo}` returns the same structure as
`--json`, with `owner`/`repo` echoed back. Optional `?pages=N` fetches more than
one page of events. Interactive docs are at `http://localhost:8000/docs`.

## Output shape

```json
{
  "baseline": {
    "event_count": 26,
    "event_type_counts": { "PushEvent": 2, "IssueCommentEvent": 4 },
    "weekly_activity": [{ "week": "2026-07-05", "events": 13 }]
  },
  "ri1": {
    "version": "0.1.0",
    "harmonic_coherence_index": 2.0,
    "notes": "ratio of code events (Push/PullRequest) to discussion events (IssueComment)"
  }
}
```

See [`COMPARISON.md`](COMPARISON.md) for these metrics run across four
repositories, with the raw payloads in [`samples/`](samples/).

## Metric contracts

### `baseline.event_count`

- **Inputs**: `GET /repos/{owner}/{repo}/events` — the length of the returned
  array.
- **Formula**: the number of events returned for the window (see the caveat
  below); with `pages > 1`, the total across all fetched pages.
- **Interpretation**: a raw volume figure. High means the repository produced a
  lot of public activity recently; low means it is quiet or the window is empty.
  It is a denominator for the other metrics, not a quality signal on its own.

### `baseline.event_type_counts`

- **Inputs**: the `type` field of each event (`PushEvent`, `PullRequestEvent`,
  `IssueCommentEvent`, `WatchEvent`, …). Events with no `type` are counted as
  `UnknownEvent`.
- **Formula**: a frequency count of `type` across all fetched events.
- **Interpretation**: shows the *mix* of work. A profile dominated by
  `PushEvent` suggests solo, commit-driven development; a spread across
  `PullRequestEvent`, `PullRequestReviewEvent`, and `IssueCommentEvent` suggests
  collaborative review activity.

### `baseline.weekly_activity`

- **Inputs**: the `created_at` timestamp of each event, parsed as UTC. Events
  with an unparsable timestamp are dropped.
- **Formula**: timestamps are resampled with pandas `resample("W")` and counted,
  producing one entry per calendar week labelled by the week-ending (Sunday)
  date. Weeks with no events are still emitted as `0`, so gaps are visible.
- **Interpretation**: high and steady counts indicate sustained engagement; a
  single tall spike surrounded by zeros indicates burst-style or abandoned work.

### `ri1.harmonic_coherence_index`

- **Inputs**: event `type` only. Code events are `PushEvent` and
  `PullRequestEvent`; discussion events are `IssueCommentEvent`. All other types
  are ignored.
- **Formula**: `len(code_events) / len(discussion_events)`. When there are no
  discussion events the result is `inf` if any code events exist and `0.0`
  otherwise; `inf` is serialized as `null` because JSON has no infinity literal.
  A `0.0` result is therefore ambiguous between "only discussion" and "no
  relevant events at all" — read it alongside `event_count`.
- **Interpretation**: high means code output dominates conversation (fast
  shipping, or little review/discussion); low means conversation dominates code
  (heavy deliberation, or stalled delivery). It is a ratio, so it is only
  meaningful for repositories with a non-trivial `event_count`. This is a
  placeholder formulation of RI1 and is expected to evolve; the `version` field
  in the `ri1` block identifies which formulation produced a given number.

**Window caveat (applies to every metric above)**: the GitHub events API only
serves roughly the last 90 days and at most 300 events, so these are metrics
over a recent window, not full repository history.

## Tests

```bash
cd metrics
python -m pytest tests -q
```

The tests use hand-written synthetic event lists (no network) and assert exact
weekly counts and coherence values for the empty, code-only, discussion-only,
and mixed cases.

## Files

| File | Purpose |
| --- | --- |
| `github_events.py` | `fetch_repo_events(owner, repo, token=None, ...)` |
| `metrics_baseline.py` | `weekly_activity`, `event_type_counts`, `activity_to_dict`, `activity_to_json` |
| `ri1_overlay.py` | `harmonic_coherence_index`, `coherence_to_dict`, `coherence_to_json` |
| `version.py` | `METRICS_VERSION` |
| `main.py` | CLI entry point |
| `api.py` | FastAPI service |
| `tests/` | pytest suite |
