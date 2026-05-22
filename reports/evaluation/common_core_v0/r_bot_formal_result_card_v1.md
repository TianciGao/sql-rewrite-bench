# R-Bot Formal Result Card v1

## Identity

- `method_id = r_bot`
- `route_id = r_bot_same_engine_rewrite`

## Generation Layer

- Formal generation denominator: `common_core_v0_40_same_engine_120`
- Planned generation rows: `120`
- `generated = 7`
- `failed = 2`
- `blocked = 31`
- `unsupported = 80`

Generated row list:

- `PERF_0006:pg`
- `PERF_0008:pg`
- `PERF_0013:pg`
- `PERF_0017:pg`
- `PERF_0024:pg`
- `PERF_0052:pg`
- `PERF_0054:pg`

Failed row list:

- `PERF_0019:pg`
- `PERF_0033:pg`

## Execution Layer

- Execution denominator: `generated_pg7_only`
- `executed = 7`
- `match_exact = 7`
- `mismatch = 0`

## Timing Layer

- Timing denominator: `generated_pg7_match_exact_only`
- `timing_success = 7`
- `GM_Speedup` over PG7 only: `0.947444`
- `RegressionRate@20%` over PG7 only: `28.57%`

Material regression rows:

- `PERF_0006`
- `PERF_0054`

## Denominator Caveat

This result card is denominator-aware:

- this is not full `120`-row timing
- this is not tri-engine timing
- this is not leaderboard-comparable without denominator labels

The retained timing evidence is limited to the seven PostgreSQL rows that were both generated and `match_exact` in execution.

## Recommended Paper Wording

Recommended wording:

`On the frozen common_core_v0_40 same-engine denominator (120 planned rows = 40 cases x 3 engines), the recovered formal R-Bot route produced 7 PostgreSQL generations, 2 PostgreSQL generation failures, 31 PostgreSQL blocked rows, and 80 mysql/spark unsupported rows. All 7 generated PostgreSQL rows passed exact-match execution validity. Timing evidence is available only for this generated_pg7_match_exact_only subset, where GM_Speedup = 0.947444 and RegressionRate@20% = 28.57% (2/7). These timing figures are subset-scoped and are not directly comparable to full-denominator or tri-engine leaderboard results without explicit denominator labels.`
