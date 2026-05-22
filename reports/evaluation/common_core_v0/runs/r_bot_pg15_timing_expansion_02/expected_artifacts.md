# Expected Artifacts

The human-run timing script is expected to create:

- `reports/evaluation/common_core_v0/runs/r_bot_pg15_timing_expansion_02/run_results.json`
- `reports/evaluation/common_core_v0/runs/r_bot_pg15_timing_expansion_02/logs/*.stdout.log`
- `reports/evaluation/common_core_v0/runs/r_bot_pg15_timing_expansion_02/logs/*.stderr.log`
- `reports/evaluation/common_core_v0/runs/r_bot_pg15_timing_expansion_02/workspaces/<case_id>/pg/r_bot_same_engine_rewrite/`
- `reports/evaluation/common_core_v0/runs/r_bot_pg15_timing_expansion_02/timings/<case_id>/pg/r_bot_same_engine_rewrite.json`

Per-row timing JSON should record:

- `source_runtime_ms`
- `generated_runtime_ms`
- `median_source_ms`
- `median_generated_ms`
- `speedup_ratio`
- `timing_status`
- `warmup_count`
- `repeat_count`
- `notes` when a timing failure occurs

This package is timing-only for the fifteen PG rows that already passed
execution validity with `match_exact` in the PG40 expansion path.

This package does not create:

- final `GM_Speedup`
- final `RegressionRate@20%`
- `same_engine_leaderboard.csv`
- method comparison summary updates
- any replacement for the existing PG7 retained timing evidence
