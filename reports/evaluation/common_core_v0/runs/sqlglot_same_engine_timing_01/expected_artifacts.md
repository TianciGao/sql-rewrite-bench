**Expected Artifacts**
Human execution of [run_manual_sqlglot_timing.sh](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/sqlglot_same_engine_timing_01/run_manual_sqlglot_timing.sh) should produce these run-local artifacts:

- `logs/env_check.stdout.log`
- `logs/env_check.stderr.log`
- `logs/<case>__<engine>__<route>.stdout.log`
- `logs/<case>__<engine>__<route>.stderr.log`
- `workspaces/<CASE>/<engine>/<route>/`
- `timings/<CASE>/<engine>/<route>.json`
- `records.tmp.jsonl`
- `run_results.json`

Per-row timing JSON should minimally contain:
- `case_id`
- `engine`
- `route_id`
- `warmup_count`
- `repeat_count`
- `source_runtime_ms`
- `generated_runtime_ms`
- `median_source_ms`
- `median_generated_ms`
- `speedup_ratio`
- `status`
- `notes`

`run_results.json` should contain:
- package-level run metadata
- `warmup_count=1`
- `repeat_count=3`
- one record per executed timing row
- explicit failure records when timing fails

This package should not produce:
- final `run_event_long.csv`
- final `method_case_summary.csv`
- `same_engine_leaderboard.csv`
- final `GM_Speedup`
- final `RegressionRate@20%`
