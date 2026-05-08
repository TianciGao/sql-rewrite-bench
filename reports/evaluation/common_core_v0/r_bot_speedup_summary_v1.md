# R-Bot Speedup Summary v1

## Scope

This summary materializes denominator-aware speedup evidence for:

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`
- generation denominator = `common_core_v0_40_same_engine_120`
- timing denominator = `generated_pg7_match_exact_only`

Boundary:

- This is PG7-only timing and speedup evidence.
- This is not full `120`-row timing.
- This is not tri-engine timing.
- This is not leaderboard-comparable without explicit denominator labels.

## Coverage Context

- planned generation rows: `120`
- generated rows: `7`
- match_exact execution rows: `7`
- timing_success rows: `7`

## Headline Speedup

- `GM_Speedup` over PG7 only: `0.947444`
- `RegressionRate@20%` over PG7 only: `28.57%` (`2 / 7`)

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

## High Variance Watchlist

- `PERF_0008`
- `PERF_0013`
- `PERF_0024`
- `PERF_0052`

## Interpretation

- The retained PG7 geometric mean speedup is below `1.0`, so this subset is net regressive on timing.
- Only `PERF_0017` shows a clear directional speedup, and it still does not exceed a `20%` speedup threshold.
- Two rows, `PERF_0006` and `PERF_0054`, fall below the `0.8` threshold and therefore count toward `RegressionRate@20%`.

## Boundary

- This summary must not be presented as full-coverage same-engine timing on the `120`-row denominator.
- It must not be presented as tri-engine timing.
- It must not be merged into a leaderboard row without carrying its narrower timing denominator explicitly.
