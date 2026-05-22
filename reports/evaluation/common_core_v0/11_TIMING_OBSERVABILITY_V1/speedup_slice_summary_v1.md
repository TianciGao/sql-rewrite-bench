# Speedup Slice Summary v1

## Purpose

这个文件回答什么问题：把 Section 8.7.1 的 correctness-gated timing slices 做成 denominator-aware route ledger，明确速度解释只建立在 exact + timing-success rows 上。

## Timing denominator rule

- Speedup is interpreted only on exact + timing-success rows.
- Every route keeps its own retained timing denominator.
- Different route roles and denominators mean this is not a ranked leaderboard.

## Route-level speedup table

| method_id | route_id | timing_denominator | gm_speedup | median_speedup | win_count | tie_count | loss_count | regression_rate_20pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| direct_llm | direct_llm_same_engine_rewrite | 94 | 1.043634242319266 | 1.009402551073825 | 22 | 67 | 5 | 0.03191489361702127 |
| direct_llm | direct_llm_execute_repair_1shot | 96 | 1.0430582867389244 | 1.009402551073825 | 23 | 67 | 6 | 0.041666666666666664 |
| sqlglot | sqlglot_optimize_same_dialect | 63 | 0.9907164888740984 | 0.9951145947521497 | 11 | 37 | 15 | 0.015873015873015872 |
| sqlglot | sqlglot_transpile_same_dialect_noop | 72 | 1.000145903000493 | 1.0020975938941747 | 10 | 51 | 11 | 0.013888888888888888 |
| calcite_hep | calcite_hep_fail_closed_120 | 93 | 0.995917121478 | 0.999279423532 | 12 | 66 | 15 | 0.0752688172043 |
| r_bot | r_bot_same_engine_rewrite | 15 | 0.9218248321470981 | 0.9820746516046041 | 1 | 7 | 7 | 0.2 |
| sqlglot | sqlglot_combined_same_engine_240 | 137 | 1.0179 | needs_per_case_timing_aggregation | needs_per_case_timing_aggregation | needs_per_case_timing_aggregation | needs_per_case_timing_aggregation | 0.0511 |

## Main observations

- `direct_llm_same_engine_rewrite` retains a `94`-row exact timed slice with `GM=1.043634242319266` and `Regression@20=0.03191489361702127`.
- `direct_llm_execute_repair_1shot` retains a mixed-source `96`-row final exact slice with `GM=1.0430582867389244`; the exact frontier improved by two rows, but speedup remains route-local to the exact timed subset.
- `sqlglot_transpile_same_dialect_noop` stays near neutral at `GM=1.000145903000493` on `72` exact timed rows.
- `sqlglot_optimize_same_dialect` retains the revised paper-safe exact63 timing slice with `GM=0.9907164888740984`.
- `calcite_hep_fail_closed_120` uses the `93` exact-row correctness-gated timing packet only, not full-120 timing.
- `r_bot_same_engine_rewrite` remains bounded appendix timing on a `PG15` subset.
- `sqlglot_combined_same_engine_240` remains an aggregate route-family view rather than a single 120-row method row.

## Denominator cautions

- The timing denominator is route-local, not shared across all rows.
- SQLGlot combined is a diagnostic aggregate and not a main same-engine method row.
- Bounded prior methods remain bounded appendix evidence.
- Mixed-source repair timing should not be restated as a single fresh route-local timing experiment.

## What this supports

- Denominator-aware speedup characterization for retained exact timed slices.
- Route-local GM, median, best/worst case, and Regression@20 reporting where Table 6 already retains them.

## What this does not support

- A ranked leaderboard.
- Full-denominator speedup claims on non-exact rows.
- Cross-route winner claims from incompatible denominators.
- Fabricated per-case timing arrays where only route summaries are retained.

## Safe prose snippet for the paper

Correctness is a precondition for speed interpretation. Correct rewrites do not automatically imply speedup, and GM plus Regression@20 are interpreted only on each route's exact timed rows. Because route roles and timing denominators differ, these slices characterize behavior rather than forming a ranked leaderboard.
