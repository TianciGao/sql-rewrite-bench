# R-Bot PG7 Speedup Summary v1

## Scope

This summary materializes speedup evidence only for the retained R-Bot PostgreSQL subset with:

- `denominator_id = generated_pg7_match_exact_only`
- source generation denominator = `common_core_v0_40_same_engine_120`

Boundary:

- This is PG7-only speedup evidence.
- This is not full `120`-row timing.
- This is not tri-engine evidence.
- This is not a leaderboard.
- This must not be compared as if it matched a PG40 denominator unless denominator mismatch is made explicit.

## Summary

- Planned timing rows: `7`
- `timing_success` rows: `7`
- `GM_Speedup` over PG7 only: `0.947444`
- `RegressionRate@20%` over PG7 only: `2 / 7 = 28.57%`

## Per-Row Speedup Ratios

- `PERF_0006:pg`: `0.765675`
- `PERF_0008:pg`: `0.999886`
- `PERF_0013:pg`: `0.997015`
- `PERF_0017:pg`: `1.135677`
- `PERF_0024:pg`: `0.995830`
- `PERF_0052:pg`: `1.001245`
- `PERF_0054:pg`: `0.792863`

## Material Regression Rows

- `PERF_0006`
- `PERF_0054`

These two rows fall below the `1 / 1.2 = 0.833333` threshold used for `RegressionRate@20%`.

## High Variance Watchlist

- `PERF_0008`
- `PERF_0013`
- `PERF_0024`
- `PERF_0052`

These rows are near parity on median timing but include visibly elevated repeats in the retained timing payloads, so they should be treated cautiously in any narrative interpretation.

## Interpretation

For this seven-row PG subset, the retained geometric mean speedup is below `1.0`, so the subset is net regressive on timing. Only one row, `PERF_0017`, shows a clear speedup directionally, and even that row does not exceed a `20%` speedup threshold.
