# Direct LLM Same-Engine Spark Timing Retry

This package is a human-run retry bundle for five Spark timing rows from the full Direct LLM same-engine timing run that failed with Spark `ParseException` during setup or loading.

Scope:

- `PERF_0008 / spark`
- `PERF_0013 / spark`
- `PERF_0017 / spark`
- `PERF_0019 / spark`
- `PERF_0024 / spark`

Inputs are unchanged:

- original generated SQL from `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/generated/`
- original case schema and witness files under `cases/`

This package changes only the Spark timing runner behavior:

- schema and witness SQL are executed as semicolon-delimited statements
- comment-only fragments and empty fragments are ignored
- multi-line DDL is preserved
- source and generated SQL are executed as one full query each

Run entrypoint:

- [run_manual_direct_llm_spark_perf5_retry.sh](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_retry_spark_perf5_01/run_manual_direct_llm_spark_perf5_retry.sh)

This package does not execute automatically. It does not compute final `GM_Speedup`, final `RegressionRate@20%`, or any leaderboard.
