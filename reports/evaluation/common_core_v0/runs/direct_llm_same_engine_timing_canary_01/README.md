# Direct LLM Same-Engine Timing Canary

This directory contains the human-run timing canary package for Direct LLM same-engine Common-core v0 measurement.

Contents:

- `timing_canary_plan.md`
- `timing_command_matrix.csv`
- `run_manual_direct_llm_timing_canary.sh`
- `expected_artifacts.md`

Scope:

- cases: `PERF_0006`, `CONS_0010`, `LONGTAIL_0011`
- engines: `pg`, `mysql`, `spark`
- route: `direct_llm_same_engine_rewrite`
- planned rows: `9`

Boundary:

- this package does not execute anything by itself
- this package does not compute final `GM_Speedup`
- this package does not compute final `RegressionRate@20%`
- this package does not create any leaderboard
