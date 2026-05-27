# SQLGlot Full Per-Case Timing Result Card v1

This is route-separated SQLGlot per-case timing after checker backfill.

- SQLGlot no-op uses 72 exact rows.
- SQLGlot optimize uses revised 63 exact rows, not the prior aggregate 65.
- The two optimize checker_failed rows are excluded from timing and remain visible in the checker backfill packet.
- No SQLGlot generation was rerun.
- No checker was rerun in this timing step.
- This does not create a final ranked leaderboard.

## Table

| method_id | route_id | timing_denominator_id | exact_rows_after_backfill | timing_success_rows | median_speedup | gm_speedup | regression_rate_20pct | claim_boundary | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sqlglot | sqlglot_transpile_same_dialect_noop | sqlglot_transpile_same_dialect_noop_exact72_timing | 72 | 72 | 1.0020975938941747 | 1.000145903000493 | 0.013888888888888888 | route-separated SQLGlot per-case timing after checker backfill; no combined main row; no final ranked leaderboard | No-op uses the full 72-row exact denominator after checker backfill. |
| sqlglot | sqlglot_optimize_same_dialect | sqlglot_optimize_same_dialect_exact63_timing | 63 | 63 | 0.9951145947521497 | 0.9907164888740984 | 0.015873015873015872 | route-separated SQLGlot per-case timing after checker backfill; no combined main row; no final ranked leaderboard | Optimize uses revised 63-row exact denominator after excluding the two checker_failed rows. |
