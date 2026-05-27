# Direct LLM Same-Engine Timing Resolved

This package materializes the resolved Direct LLM same-engine timing evidence for Common-core v0.

Scope:

- `denominator_id = common_core_v0_40`
- `method_id = direct_llm`
- `route_id = direct_llm_same_engine_rewrite`
- `planned rows = 120`
- `timing_eligible rows = 94`
- `resolved timing_success rows = 94`

Provenance:

- `89` timing-success rows are retained from `direct_llm_same_engine_timing_01`
- `5` Spark timing rows are replaced from `direct_llm_same_engine_timing_retry_spark_perf5_01`
- the replaced rows were original full-run Spark timing-loader failures and were resolved by the targeted retry package

Outputs:

- [run_manifest.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_resolved_01/run_manifest.json)
- [timing_event_long.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_resolved_01/timing_event_long.csv)
- [timing_case_summary.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_resolved_01/timing_case_summary.csv)
- [validation_report.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_resolved_01/validation_report.json)
- [materialization_notes.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_resolved_01/materialization_notes.md)

This package does not compute final `GM_Speedup`, final `RegressionRate@20%`, or any leaderboard.
