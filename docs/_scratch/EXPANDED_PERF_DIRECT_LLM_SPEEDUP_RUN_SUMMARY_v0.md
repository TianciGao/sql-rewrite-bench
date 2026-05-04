# EXPANDED_PERF_DIRECT_LLM_SPEEDUP_RUN_SUMMARY_v0

## Status

This note records the current expanded PERF Direct LLM speedup runtime/scoring result for:

- `reports/formal_expansion/expanded_perf_direct_llm_speedup_run_v0.json`

Result status:

- full expanded PERF PostgreSQL-side speedup run completed
- executed: `34 / 34`
- success: `34 / 34`
- failed: `0 / 34`
- valid speedup cases: `34`
- row-count matches: `34 / 34`
- no model calls during speedup scoring

## Scope

- denominator: expanded PERF `34`
- route: `LLM_DIRECT_REWRITE_STRONG`
- engine: PostgreSQL only
- token usage carried from the prior Direct LLM run: `29414`
- claim boundary: `expanded_perf_direct_llm_speedup_run_postgres_only_not_final_leaderboard`

Runtime policy configured in the command artifact:

- `warmup_count=1`
- `repeat_count=5`
- `statement_timeout_ms=30000`
- `primary_statistic=median`
- `tie_threshold=0.05`
- `regression_threshold=1.2`

## Reported Run State

- `ok=true`
- denominator surfaced: `34`
- executed count: `34`
- failed count: `0`
- `valid_speedup_case_count=34`
- candidate SQL source: prior Direct LLM run report `extracted_sql_text`
- no model calls
- no plan collection
- no registry writeback
- no case artifact write

## Metrics

- `GM_Speedup=1.0029707606749427`
- `W/T/L=7 / 19 / 8`
- `RegressionRate@20%=0.0`
- `total_token_usage=29414`

Interpretation:

- Direct LLM expanded PERF is now checker-backed and speedup-scored.
- runtime effect is near-neutral and tie-heavy.
- no `20%` regression was observed.
- this should not be framed as a strong speedup result.

## Row-Count Match Summary

- row-count match count: `34 / 34`
- row-count mismatch count: `0 / 34`
- all scored cases remained checker-aligned with the source query output cardinality

## Execution Summary

- denominator: `34`
- executed: `34 / 34`
- success: `34 / 34`
- failed: `0 / 34`
- failure categories: none
- issues reported by artifact: none

## Boundaries

- PostgreSQL-only
- expanded PERF only
- no model calls during speedup scoring
- not a final leaderboard
- no registry changes
- no `docs/EXECUTION_STATUS.md` changes
- no formal review changes
- no case file changes
- no taxonomy calibration note changes

## Verification / Non-Modification Note

- this note only records the existing formal report
- no experiment was run for this documentation update
- no model / LLM call was made
- no SQL execution was performed
- no checker execution was performed
- no registry / status / review writeback occurred
