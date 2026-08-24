# Cross-repository comparison (metrics v0.1.0)

Captured 2026-07-24 with an authenticated token, one page of events per repo
(`python main.py --owner <owner> --repo <repo> --json`). Raw payloads are in
[`samples/`](samples/). Numbers move as the underlying window moves; re-run the
command to refresh.

## Baseline

| Repository | `event_count` | Event type mix | Weekly activity (week ending: events) |
| --- | --- | --- | --- |
| `Andrewkadz/HARMONIA-DSL` | 29 | PullRequestEvent 6, CreateEvent 6, PullRequestReviewCommentEvent 5, PushEvent 5, IssueCommentEvent 4, PullRequestReviewEvent 2, WatchEvent 1 | 07-05: 13, 07-12: 0, 07-19: 9, 07-26: 7 |
| `Andrewkadz/RI1-HYBRID-ENGINE` | 0 | — | — |
| `chaoss/grimoirelab` | 23 | WatchEvent 14, PullRequestEvent 5, ForkEvent 3, CreateEvent 1 | 06-28: 4, 07-05: 3, 07-12: 3, 07-19: 5, 07-26: 8 |
| `pallets/flask` | 94 | WatchEvent 60, ForkEvent 19, PullRequestEvent 9, PullRequestReviewEvent 4, IssueCommentEvent 2 | 07-26: 94 |

## RI1

| Repository | `harmonic_coherence_index` | `recommended_lever` | Current vs target | Severity |
| --- | --- | --- | --- | --- |
| `Andrewkadz/HARMONIA-DSL` | 2.75 | `review_throughput` | 276.5h vs 48h | 5.76 |
| `Andrewkadz/RI1-HYBRID-ENGINE` | 0.0 | `issue_closure_ratio` | 0.00 vs 0.50 | 3.00 |
| `chaoss/grimoirelab` | `null` (∞) | `discussion_density` | 0.00 vs 0.20 | 2.00 |
| `pallets/flask` | 4.5 | none | — | — |

## Reading of the numbers

- `HARMONIA-DSL` shows 29 events across four weeks with one empty week, a mix
  dominated by pull-request and review activity, and coherence 2.75. Its lever
  is `review_throughput` at 276h, but from a sample of one closed PR — the
  number is real, its representativeness is not.
- `RI1-HYBRID-ENGINE` returns zero events. Its last push was 2025-12-11, outside
  the events API's ~90-day window, so all baseline metrics are empty. The lever
  still resolves because issues are fetched separately: three open issues, none
  closed. Note the `0.0` coherence here means "no relevant events", not
  "discussion-heavy" — read it alongside `event_count`.
- `chaoss/grimoirelab` shows 23 events spread evenly across five weeks — the
  steadiest weekly profile of the four — but most of that volume is
  `WatchEvent`/`ForkEvent` (attention, not authorship). Coherence is undefined
  because the window holds PRs and no issue comments; the same absence drives
  the `discussion_density` lever to 0.0 off a sample of 5 events. Its
  `review_throughput` (24.7h median, n=100) and `issue_closure_ratio` (0.39,
  n=31) are the better-evidenced figures here.
- `pallets/flask` has no out-of-band lever: 0.2h median PR close time, 88%
  issue closure, 0.67 discussion per code event — every candidate is inside its
  target band. Its 94 events all land in a single week, which is a window
  artifact rather than a burst: one page (100 events) of a high-traffic
  repository only reaches back 4 days.

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
- Levers are selected by severity alone and ignore `sample_size`, so a single
  slow PR can outrank a well-evidenced signal (see `HARMONIA-DSL` above). Read
  `sample_size` before acting on a recommendation.
