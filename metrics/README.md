# metrics

Compute activity and a first RI1 coherence metric for HARMONIA-DSL using GitHub events.

Everything here is deterministic: it reads the public GitHub REST events API
(`/repos/{owner}/{repo}/events`) and derives numbers from it. No LLM calls.

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

## Outputs

- **Weekly event counts** — how many GitHub events landed in each calendar week
  (weeks are bucketed with `resample("W")`, labelled by the week-ending date).
  A week with zero events still appears, so gaps in activity are visible.
- **Harmonic coherence index** — `code events / discussion events`, where code
  events are `PushEvent` and `PullRequestEvent` and discussion events are
  `IssueCommentEvent`. High values mean commits outpace conversation; low values
  mean the reverse. It is `inf` (`null` in JSON) when there are code events but
  no discussion, and `0.0` when there are neither. This is a placeholder
  formulation of RI1 and is expected to evolve.

Note: the events API only returns roughly the last 90 days (max 300 events), so
the weekly series is a recent window, not full repository history.

## HTTP API

```bash
cd metrics
uvicorn api:app --reload --port 8000
```

Then request `http://localhost:8000/metrics/Andrewkadz/HARMONIA-DSL`, which
returns the event count, CHAOSS-style per-type event counts, the weekly activity
series, and the coherence index in one JSON payload. Interactive docs are at
`http://localhost:8000/docs`.

## Files

| File | Purpose |
| --- | --- |
| `github_events.py` | `fetch_repo_events(owner, repo, token=None, ...)` |
| `metrics_baseline.py` | `weekly_activity`, `activity_to_dict`, `activity_to_json` |
| `ri1_overlay.py` | `harmonic_coherence_index`, `coherence_to_dict`, `coherence_to_json` |
| `main.py` | CLI entry point |
| `api.py` | FastAPI service |
