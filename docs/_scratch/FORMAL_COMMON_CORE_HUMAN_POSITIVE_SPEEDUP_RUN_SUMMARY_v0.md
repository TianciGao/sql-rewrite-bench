# FORMAL_COMMON_CORE_HUMAN_POSITIVE_SPEEDUP_RUN_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of the `HUMAN_REFERENCE_POSITIVE` PERF-only formal speedup run.

This is a positive-control speedup run only.

## 2. Policy Used

Frozen first-pass policy used:

- `repeat_count=5`
- `warmup_count=1`
- `statement_timeout_ms=30000`
- `primary_runtime_statistic=median`
- auxiliary runtime statistics: `min`, `mean`
- `tie_threshold=0.05`
- `regression_threshold=1.2`

## 3. Denominator

PERF-only denominator:

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`

## 4. Execution Result

- `case_count=7`
- `executed_case_count=7`
- `success_count=7`
- `failed_count=0`
- `formal_speedup_scoring_complete=true`

## 5. Per-Case Runtime Table

| case_id | source_median_ms | candidate_median_ms | speedup_ratio | win_tie_loss | regression_20pct |
|---|---:|---:|---:|---|---|
| `PERF_0006` | `0.261` | `0.291` | `0.8969` | `loss` | `false` |
| `PERF_0008` | `0.326` | `0.346` | `0.9422` | `loss` | `false` |
| `PERF_0013` | `0.617` | `0.633` | `0.9747` | `tie` | `false` |
| `PERF_0017` | `0.381` | `0.381` | `1.0` | `tie` | `false` |
| `PERF_0024` | `0.37` | `0.34` | `1.0882` | `win` | `false` |
| `PERF_0033` | `0.285` | `0.309` | `0.9223` | `loss` | `false` |
| `PERF_0054` | `0.297` | `0.323` | `0.9195` | `loss` | `false` |

## 6. GM_Speedup / Win-Tie-Loss / RegressionRate@20%

- `gm_speedup=0.96159127168004`
- `win_count=1`
- `tie_count=2`
- `loss_count=4`
- `regression_20pct_count=0`

## 7. Row-Count Match Observations

- `row_count_match_count=7`
- `row_count_mismatch_count=0`

All PERF cases matched source row count in this positive-control run.

## 8. Claim Boundaries

- positive-control speedup only
- PERF-only
- not the full leaderboard
- SQLGlot and Direct LLM speedup remain blocked
- CONS excluded
- no registry writeback
- no formal review update

## 9. Recommended Next Action

- decide whether to run an exploratory row-count-gated SQLGlot / Direct LLM speedup appendix, or first build method-specific checker-backed consistency artifacts
