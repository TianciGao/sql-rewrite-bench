# Materialization Notes

## Resolution Summary

This resolved package merges the original full Direct LLM timing run with the targeted Spark retry package.

- original full timing successes: `89`
- targeted retry successes: `5`
- resolved timing successes: `94 / 94` timing-eligible rows
- timing failures after retry: `0`

## Replacement Rows

Only these five rows were replaced by retry timing outputs:

- `PERF_0008 / spark / direct_llm_same_engine_rewrite`
- `PERF_0013 / spark / direct_llm_same_engine_rewrite`
- `PERF_0017 / spark / direct_llm_same_engine_rewrite`
- `PERF_0019 / spark / direct_llm_same_engine_rewrite`
- `PERF_0024 / spark / direct_llm_same_engine_rewrite`

## Provenance Interpretation

The original full-run failures for those five rows were Spark timing-runner loader failures, not Direct LLM generated-SQL validity failures.

Evidence preserved in the original full timing logs shows Spark `ParseException` with `[PARSE_SYNTAX_ERROR] Syntax error at or near end of input.` The targeted retry package succeeded after correcting the Spark loader to execute setup SQL as semicolon-delimited statements while preserving full-query execution for `source.sql` and generated SQL.

## Excluded Rows Still Explicit

These rows remain excluded from timing because they were not timing-eligible in the preflight package:

- `execution_failed = 16`
- `mismatch = 5`
- `preflight_blocked_missing_artifact = 5`

This package is timing evidence materialization only. It does not compute final `GM_Speedup`, final `RegressionRate@20%`, or any leaderboard.

## Validation Result

- `timing_event_long row count = 94`
- `distinct timing-eligible rows = 94`
- `missing timing rows = 0`
- `duplicate timing rows = 0`
- `ok = true`
