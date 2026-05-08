# Direct LLM Spark Timing Retry Plan

## Scope

This package is a targeted human-run retry for the five Spark timing rows that failed in the full Direct LLM same-engine timing run due to an apparent Spark timing-runner SQL loading issue:

- `PERF_0008 / spark / direct_llm_same_engine_rewrite`
- `PERF_0013 / spark / direct_llm_same_engine_rewrite`
- `PERF_0017 / spark / direct_llm_same_engine_rewrite`
- `PERF_0019 / spark / direct_llm_same_engine_rewrite`
- `PERF_0024 / spark / direct_llm_same_engine_rewrite`

These rows were `match_exact` during the Direct LLM execution and validity phase. This retry therefore treats the prior failures as runner or setup failures first, not as generated-SQL method failures.

## Purpose

- re-run only the five failed Spark timing rows
- use the corrected Spark SQL loader
- preserve warmup and repeat settings from the full timing plan
- capture retry-local logs, per-row timing JSON, and `run_results.json`
- continue after per-row failures

## Fixed Spark Loader Behavior

The retry runner uses the corrected Spark timing loader semantics:

- `ddl_spark.sql` and `spark_witness_data.sql` are executed as semicolon-delimited statements
- splitting is not performed on lines or blank lines
- empty statements are ignored
- pure comment-only fragments are ignored
- multi-line `CREATE TABLE` statements are preserved
- `source.sql` and generated SQL are each executed as one full query statement

## Run Settings

- `method_id = direct_llm`
- `route_id = direct_llm_same_engine_rewrite`
- `engine = spark`
- `warmup_count = 1`
- `repeat_count = 3`
- human-run only
- no final `GM_Speedup`
- no final `RegressionRate@20%`
- no leaderboard generation

## Expected Outcome

If the loader issue was the real cause, these five rows should become timing-runnable without any change to generated SQL or case artifacts.
