# Cross-repository comparison (metrics v0.1.0)

Captured 2026-07-24 with an authenticated token, one page of events per repo
(`python main.py --owner <owner> --repo <repo> --json`). Raw payloads are in
[`samples/`](samples/).

## Baseline

| Repository | `event_count` | Event type mix | Weekly activity (week ending: events) |
| --- | --- | --- | --- |
| `Andrewkadz/HARMONIA-DSL` | 28 | PullRequestEvent 6, CreateEvent 6, PullRequestReviewCommentEvent 5, PushEvent 4, IssueCommentEvent 4, PullRequestReviewEvent 2, WatchEvent 1 | 07-05: 13, 07-12: 0, 07-19: 9, 07-26: 6 |
| `Andrewkadz/RI1-HYBRID-ENGINE` | 0 | — | — |
| `chaoss/grimoirelab` | 23 | WatchEvent 14, PullRequestEvent 5, ForkEvent 3, CreateEvent 1 | 06-28: 4, 07-05: 3, 07-12: 3, 07-19: 5, 07-26: 8 |
| `pallets/flask` | 94 | WatchEvent 60, ForkEvent 19, PullRequestEvent 9, PullRequestReviewEvent 4, IssueCommentEvent 2 | 07-26: 94 |

## RI1

| Repository | `harmonic_coherence_index` |
| --- | --- |
| `Andrewkadz/HARMONIA-DSL` | 2.5 |
| `Andrewkadz/RI1-HYBRID-ENGINE` | 0.0 |
| `chaoss/grimoirelab` | `null` (∞ — code events, no `IssueCommentEvent`) |
| `pallets/flask` | 4.5 |

## Reading of the numbers

- `HARMONIA-DSL` shows 28 events across four weeks with one empty week, a mix
  dominated by pull-request and review activity, and coherence 2.5 (10 code
  events to 4 issue comments). This matches a repository under active,
  PR-centric development by a small number of actors.
- `RI1-HYBRID-ENGINE` returns zero events. Its last push was 2025-12-11, which
  is outside the events API's ~90-day window, so every metric is empty. Note the
  `0.0` coherence here means "no relevant events", not "discussion-heavy" — read
  it alongside `event_count`.
- `chaoss/grimoirelab` shows 23 events spread evenly across five weeks — the
  steadiest weekly profile of the four. Most of the volume is `WatchEvent` and
  `ForkEvent` (attention, not authorship); the 5 `PullRequestEvent`s with no
  `IssueCommentEvent` make coherence infinite, which is a limitation of the
  ratio rather than a signal about the project.
- `pallets/flask` returns 94 events all inside a single week. That is a window
  artifact, not a burst: one page (100 events) of a high-traffic repository only
  reaches back to 2026-07-20. Its weekly series is therefore not comparable with
  the low-traffic repos above without paging (`--pages`/`?pages=N`).

## Caveats

- The events API serves roughly the last 90 days and at most 300 events, so busy
  repositories are truncated in *time* while quiet ones are truncated in
  *content*. Comparing weekly series across repositories of very different
  traffic requires equalising the window first.
- `WatchEvent`/`ForkEvent` inflate `event_count` for popular repositories
  without representing any authored work.
- `harmonic_coherence_index` only counts `IssueCommentEvent` as discussion, so
  projects whose conversation happens in `PullRequestReviewEvent` /
  `PullRequestReviewCommentEvent` look artificially code-heavy, and any window
  with zero issue comments collapses to `null`. This is a known limitation of
  v0.1.0.
