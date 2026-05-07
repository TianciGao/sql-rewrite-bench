# LONGTAIL SQLStorm Common-core Review-prep

## Executive Summary

This is a focused read-only review-prep on the SQLStorm LONGTAIL candidates for possible Common-core v0 use. It does not change registry state and does not make final admission decisions.

Current non-SQLStorm LONGTAIL context already in the working mix: `LONGTAIL_0022, LONGTAIL_0023, LONGTAIL_0024`. These three cases cover comments, post-links, and post-history substrate patterns rather than the user/post ranking and badge/vote rollups seen in the SQLStorm line.

Suitability counts: `strong_longtail_review_candidate=3`, `acceptable_with_manual_review=3`, `extended_preferred=4`, `defer=0`.

The strongest review-prep trio is `LONGTAIL_0011`, `LONGTAIL_0012`, and `LONGTAIL_0013`. They are all tri-engine artifact-complete, have clear SQLStorm provenance, and add distinct feature families beyond the existing Stack-substrate longtail cases. The main reason they were previously held back is registry lag (`not_assessed`), not missing package evidence.

## Candidate Table

| case_id | benchmark_line | admission_status | tri_engine | result_check | plan_check | diversity vs 0022/0023/0024 | duplicate-ish | suitability |
|---|---|---|---|---|---|---|---|---|
| `LONGTAIL_0011` | `not_assessed` | `not_assessed` | `yes` | yes | yes | adds window/ranking behavior absent from LONGTAIL_0022/0023/0024 | low: unique max-rank-per-owner pattern in this candidate set | `strong_longtail_review_candidate` |
| `LONGTAIL_0012` | `not_assessed` | `not_assessed` | `yes` | yes | yes | adds Votes-derived signal absent from LONGTAIL_0022/0023/0024 | adds window/ranking behavior absent from LONGTAIL_0022/0023/0024 | adds HAVING-filtered aggregate behavior absent from LONGTAIL_0022/0023/0024 | adds AVG-based scoring aggregation absent from LONGTAIL_0022/0023/0024 | low: unique votes subquery plus AVG metrics pattern in this candidate set | `strong_longtail_review_candidate` |
| `LONGTAIL_0013` | `not_assessed` | `not_assessed` | `yes` | yes | yes | adds Votes-derived signal absent from LONGTAIL_0022/0023/0024 | adds Badges-derived signal absent from LONGTAIL_0022/0023/0024 | adds window/ranking behavior absent from LONGTAIL_0022/0023/0024 | adds HAVING-filtered aggregate behavior absent from LONGTAIL_0022/0023/0024 | adds AVG-based scoring aggregation absent from LONGTAIL_0022/0023/0024 | moderate: close to sibling in votes/badges/ranked-posts cluster | `strong_longtail_review_candidate` |
| `LONGTAIL_0005` | `not_assessed` | `not_assessed` | `yes` | yes | yes | still differs from LONGTAIL_0022/0023/0024 by focusing on Users/Posts ranking instead of Comments/PostLinks/PostHistory substrate | moderate: simpler aggregate cousin of broader user-post rollup cases | `acceptable_with_manual_review` |
| `LONGTAIL_0014` | `not_assessed` | `not_assessed` | `yes` | yes | yes | adds Votes-derived signal absent from LONGTAIL_0022/0023/0024 | adds Badges-derived signal absent from LONGTAIL_0022/0023/0024 | adds window/ranking behavior absent from LONGTAIL_0022/0023/0024 | adds HAVING-filtered aggregate behavior absent from LONGTAIL_0022/0023/0024 | moderate: close to sibling in votes/badges/ranked-posts cluster | `acceptable_with_manual_review` |
| `LONGTAIL_0015` | `not_assessed` | `not_assessed` | `yes` | yes | yes | adds window/ranking behavior absent from LONGTAIL_0022/0023/0024 | yes: highly duplicate-ish with LONGTAIL_0015/0018/0019/0020/0021 top-users aggregate/rank cluster | `acceptable_with_manual_review` |
| `LONGTAIL_0018` | `not_assessed` | `not_assessed` | `yes` | yes | yes | adds window/ranking behavior absent from LONGTAIL_0022/0023/0024 | yes: highly duplicate-ish with LONGTAIL_0015/0018/0019/0020/0021 top-users aggregate/rank cluster | `extended_preferred` |
| `LONGTAIL_0019` | `not_assessed` | `not_assessed` | `yes` | yes | yes | adds window/ranking behavior absent from LONGTAIL_0022/0023/0024 | yes: highly duplicate-ish with LONGTAIL_0015/0018/0019/0020/0021 top-users aggregate/rank cluster | `extended_preferred` |
| `LONGTAIL_0020` | `not_assessed` | `not_assessed` | `yes` | yes | yes | adds window/ranking behavior absent from LONGTAIL_0022/0023/0024 | yes: highly duplicate-ish with LONGTAIL_0015/0018/0019/0020/0021 top-users aggregate/rank cluster | `extended_preferred` |
| `LONGTAIL_0021` | `not_assessed` | `not_assessed` | `yes` | yes | yes | adds window/ranking behavior absent from LONGTAIL_0022/0023/0024 | yes: highly duplicate-ish with LONGTAIL_0015/0018/0019/0020/0021 top-users aggregate/rank cluster | `extended_preferred` |

## Recommended Three SQLStorm Candidates

- `LONGTAIL_0011`: best combination of tri-engine completeness, provenance clarity, and non-overlapping feature diversity beyond LONGTAIL_0022/0023/0024. Feature signal: `cte|window|group_by|order_by|max|where`. Tables: `maxrank|posts|rankedposts|users`.
- `LONGTAIL_0012`: best combination of tri-engine completeness, provenance clarity, and non-overlapping feature diversity beyond LONGTAIL_0022/0023/0024. Feature signal: `window|left_join|group_by|having|order_by|limit|distinct|case_when|count|sum|avg|max|where`. Tables: `posts|users|votes`.
- `LONGTAIL_0013`: best combination of tri-engine completeness, provenance clarity, and non-overlapping feature diversity beyond LONGTAIL_0022/0023/0024. Feature signal: `cte|window|left_join|group_by|having|order_by|distinct|case_when|count|sum|avg|where`. Tables: `badges|posts|rankedposts|users|userstats|votes`.

## Why These Three

- `LONGTAIL_0011` is the cleanest unique ranked-posts candidate. It introduces a two-CTE rank/max-rank pattern with window logic that does not overlap much with the Stack-substrate trio or the broader top-users rollup cluster.
- `LONGTAIL_0012` adds the strongest vote-derived aggregate signal through a nested vote-count subquery, `AVG` metrics, `HAVING`, and a ranking column. That makes it materially more diverse than the simpler user/post count cases.
- `LONGTAIL_0013` adds the richest multi-table shape in the SQLStorm set through `Votes`, `Badges`, `Posts`, `Users`, ranked-post recovery, and grouped `HAVING` logic. It is the best third pick even though it is moderately close to `LONGTAIL_0014`.

## Why The Others Rank Lower

- `LONGTAIL_0014` is acceptable but overlaps heavily with `LONGTAIL_0013` in the votes/badges/ranked-posts family.
- `LONGTAIL_0005` is acceptable but lower complexity, mainly a straightforward left-join aggregate over `Users` and `Posts`.
- `LONGTAIL_0015`, `LONGTAIL_0018`, `LONGTAIL_0019`, `LONGTAIL_0020`, and `LONGTAIL_0021` are heavily duplicate-ish top-users rollup variants. Keeping more than one of them would spend scarce LONGTAIL slots on very similar coverage.

## Review-readiness Caveat

All ten SQLStorm candidates still carry the same live-registry caveat: `benchmark_line=not_assessed` and `admission_status=not_assessed`. On package evidence alone they are tri-engine review-ready, but a narrow registry/status review is still needed before final Common-core v0 finalization if the project wants these three to count as formal common-core review candidates rather than extended-preferred drafts.

## Recommendation

Recommend exactly these 3 SQLStorm candidates for the next human common-core review-prep pass: `LONGTAIL_0011, LONGTAIL_0012, LONGTAIL_0013`.
A narrow registry/status review should align these cases from `not_assessed` into an explicit staged review line before finalizing the Common-core v0 40-case slate.

## Non-decision Statement

This report is review-prep only. It does not run databases, does not call LLM/API, does not modify registry or SQL files, and does not make final admission decisions.
