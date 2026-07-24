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

Choose an output format with `--format text|json|prometheus|oscal` (`--json` is
a shorthand for `--format json`):

```bash
python main.py --repo RI1-HYBRID-ENGINE --json
python main.py --format prometheus
```

Other flags: `--pages N` fetches more event pages, `--no-levers` skips the pull
request and issue calls (one API call instead of three), `--no-record` skips
appending to the history file.

Set `GITHUB_TOKEN` to raise the API rate limit (60 requests/hour when
unauthenticated) and to read private repositories.

## HTTP API

```bash
cd metrics
uvicorn api:app --reload --port 8000
```

| Endpoint | Returns |
| --- | --- |
| `GET /metrics/{owner}/{repo}` | the full JSON payload below |
| `GET /metrics?owner=X&repo=Y` | the same data in Prometheus exposition format |
| `GET /assessment/{owner}/{repo}` | the payload wrapped in an OSCAL-shaped assessment-results object |
| `GET /history/{owner}/{repo}` | timestamped scalars from previous runs |

All measurement endpoints accept `?pages=N` (event pages to fetch) and
`?levers=false` (skip the pull request and issue calls). Interactive docs are at
`http://localhost:8000/docs`.

## Output shape

```json
{
  "owner": "Andrewkadz",
  "repo": "HARMONIA-DSL",
  "collected_at": "2026-07-24T23:25:52+00:00",
  "baseline": {
    "event_count": 26,
    "event_type_counts": { "PushEvent": 2, "IssueCommentEvent": 4 },
    "weekly_activity": [{ "week": "2026-07-05", "events": 13 }]
  },
  "ri1": {
    "version": "0.1.0",
    "harmonic_coherence_index": 2.0,
    "notes": "ratio of code events (Push/PullRequest) to discussion events (IssueComment)",
    "recommended_lever": {
      "name": "review_throughput",
      "description": "Reduce median PR review time below 48h",
      "current_value": 276.5125,
      "target_value": 48.0,
      "unit": "hours",
      "severity": 5.7607,
      "sample_size": 1
    },
    "candidate_levers": [ ... ]
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

### `ri1.recommended_lever`

- **Inputs**: the events feed plus `GET /repos/{owner}/{repo}/pulls?state=closed`
  and `GET /repos/{owner}/{repo}/issues?state=all` (pull requests filtered out
  of the issue list).
- **Formula**: three candidate levers are computed, each with a target and a
  `severity` equal to how far the observed value sits outside that target
  (`1.0` is exactly on target, above `1.0` is out of band):

  | Lever | Value | Target | Severity |
  | --- | --- | --- | --- |
  | `review_throughput` | median hours from PR opened to closed | ≤ 48h | `value / 48` |
  | `issue_closure_ratio` | closed ÷ all recent issues | ≥ 0.5 | `0.5 / value` |
  | `discussion_density` | discussion ÷ code events, counting reviews and review comments as discussion | ≥ 0.2 | `0.2 / value` |

  Levers whose inputs are missing (no closed PRs, no issues, no code events) are
  omitted. `recommended_lever` is the surviving lever with the highest severity,
  or `null` when every candidate is inside its target band. All candidates are
  returned under `candidate_levers` so the choice can be audited.
- **Interpretation**: the single tunable parameter to move first. Selection
  ignores `sample_size`, so one slow PR can outrank a well-evidenced signal —
  check `sample_size` before acting. `discussion_density` deliberately counts
  review events, unlike `harmonic_coherence_index`.

**Window caveat (applies to every metric above)**: the GitHub events API only
serves roughly the last 90 days and at most 300 events, so these are metrics
over a recent window, not full repository history.

## Dashboards

Grafana can consume this service two ways:

- **Prometheus**: scrape `GET /metrics?owner=X&repo=Y` — the multi-target
  exporter pattern, one scrape job per repository. Exported series are
  `ri1_event_count`, `ri1_events_by_type{type}`, `ri1_weekly_events{week}`,
  `ri1_harmonic_coherence_index`, `ri1_lever_value{lever}`,
  `ri1_lever_severity{lever}`, and `ri1_recommended_lever{lever}` (1 for the
  recommended one), all labelled with `owner` and `repo`.
  `ri1_harmonic_coherence_index` is omitted rather than faked when undefined.

  ```yaml
  scrape_configs:
    - job_name: ri1
      metrics_path: /metrics
      static_configs:
        - targets: ["localhost:8000"]
      params:
        owner: [Andrewkadz]
        repo: [HARMONIA-DSL]
  ```

- **Infinity / JSON API data source**: point it at `GET /metrics/{owner}/{repo}`
  for a single snapshot, or `GET /history/{owner}/{repo}` for a time series.

Every measurement run appends one line to `history.jsonl` (override with
`METRICS_HISTORY_PATH`) holding `collected_at`, `event_count`,
`harmonic_coherence_index`, and the recommended lever's name and value. That is
the time dimension: run the CLI or hit the API on a schedule and the file
becomes a chartable series. It is git-ignored.

## OSCAL-shaped output

`GET /assessment/{owner}/{repo}` (or `--format oscal`) returns the same
measurements in OSCAL's assessment-layer vocabulary: `metadata`, `results`,
`observations` for each metric, and a `finding` with
`status.state = not-satisfied` for the recommended lever. The untouched payload
is carried alongside under `ri1-payload`. Identifiers are UUIDv5 values derived
from the repository and metric name, so the same input yields the same document.

[`oscal-component-definition.json`](oscal-component-definition.json) describes
this service as a component that exports those metrics.

Neither file is a validated OSCAL document — they adopt the *shape* so a real
OSCAL mapping later does not require reworking the service.

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
| `github_events.py` | `fetch_repo_events`, `fetch_pull_requests`, `fetch_issues` |
| `metrics_baseline.py` | `weekly_activity`, `event_type_counts`, `activity_to_dict`, `activity_to_json` |
| `ri1_overlay.py` | `harmonic_coherence_index`, `coherence_to_dict`, `coherence_to_json` |
| `levers.py` | `Lever`, `candidate_levers`, `recommended_lever` |
| `report.py` | `build_report` (fetch + assemble), `assemble_report` (offline) |
| `history.py` | `record_run`, `load_history` |
| `prometheus.py` | `render_prometheus` |
| `oscal.py` | `to_assessment_results` |
| `version.py` | `METRICS_VERSION` |
| `main.py` | CLI entry point |
| `api.py` | FastAPI service |
| `tests/` | pytest suite |
