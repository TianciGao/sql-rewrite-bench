# Expected Artifacts

The human-run timing script is expected to create:

- `reports/evaluation/common_core_v0/runs/r_bot_pg7_timing_01/run_results.json`
- `reports/evaluation/common_core_v0/runs/r_bot_pg7_timing_01/logs/*.stdout.log`
- `reports/evaluation/common_core_v0/runs/r_bot_pg7_timing_01/logs/*.stderr.log`
- `reports/evaluation/common_core_v0/runs/r_bot_pg7_timing_01/workspaces/<case_id>/pg/r_bot_same_engine_rewrite/`
- `reports/evaluation/common_core_v0/runs/r_bot_pg7_timing_01/timings/<case_id>/pg/r_bot_same_engine_rewrite.json`

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

This package is timing-only for the seven PG rows that already passed execution validity with `match_exact`.

This package does not create:

- final `GM_Speedup`
- final `RegressionRate@20%`
- `same_engine_leaderboard.csv`
- method comparison summary updates
