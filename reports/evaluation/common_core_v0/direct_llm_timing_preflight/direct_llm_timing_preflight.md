# Direct LLM @40 Timing / Speedup Preflight

## Scope

This preflight prepares the timing-bearing Direct LLM same-engine experiment for Common-core v0 without executing any timing run.

Inputs:

- `reports/evaluation/common_core_v0/direct_llm_validity_summary_v1.md`
- `reports/evaluation/common_core_v0/direct_llm_validity_summary_v1.csv`
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/run_results.json`
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/execution_triage.md`
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/execution_triage.csv`
- `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/run_results.json`
- generated Direct LLM SQL under `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01/generated/`
- `reports/evaluation/common_core_v0/controls_status/common_core_v0_controls_status_table_v2.csv`
- `reports/curation/common_core_v0_final_denominator.csv`
- `benchmark_spec/COMMON_CORE_V0_EVALUATION_PROTOCOL.md`
- SQLGlot timing runner references under `reports/evaluation/common_core_v0/runs/sqlglot_same_engine_timing_canary_01/` and `reports/evaluation/common_core_v0/runs/sqlglot_same_engine_timing_01/`

This is a preflight artifact only. It does **not** compute timing, speedup, or any leaderboard.

## Fixed Run Identity

- `denominator_id`: `common_core_v0_40`
- `method_id`: `direct_llm`
- `route_id`: `direct_llm_same_engine_rewrite`
- planned rows: `120`
- timing_eligible rows: `94`
- speedup_eligible rows: `94`
- output_directory: `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_01/`
- warmup_count: `1`
- repeat_count: `3`

## Eligibility Rule

Timing eligibility is defined strictly as:

- `timing_eligible = yes` iff validity outcome is `match_exact`

Therefore:

- `94` rows are timing-eligible and speedup-eligible
- `5` preflight-blocked rows are excluded as package/artifact gaps
- `16` execution-failed rows are excluded
- `5` mismatch rows are excluded

## Exclusion Counts

| exclusion_reason | rows |
|---|---:|
| `preflight_blocked_missing_artifact` | 5 |
| `execution_failed` | 16 |
| `mismatch` | 5 |

## Counts By Engine

| engine | total_rows | timing_eligible | execution_failed | mismatch | preflight_blocked |
|---|---:|---:|---:|---:|---:|
| `pg` | 40 | 32 | 6 | 1 | 1 |
| `mysql` | 40 | 34 | 2 | 2 | 2 |
| `spark` | 40 | 28 | 8 | 2 | 2 |

## Counts By Pool

| pool | total_rows | timing_eligible | execution_failed | mismatch | preflight_blocked |
|---|---:|---:|---:|---:|---:|
| `consistency` | 27 | 24 | 0 | 3 | 0 |
| `longtail` | 18 | 16 | 2 | 0 | 0 |
| `performance` | 48 | 45 | 2 | 1 | 0 |
| `portability` | 27 | 9 | 12 | 1 | 5 |

## Main Caveats

- PORT rows must retain portability-stress caveats even when timing-eligible.
- Preflight-blocked rows are package/artifact gaps and should not be treated as Direct LLM SQL failures.
- Execution-failed rows remain excluded from timing even when the root cause is a draft DDL/package limitation rather than the rewrite alone.
- `PERF_0077 / spark` and `PORT_0004 / spark` remain explicit draft-DDL/package-limitation failures from the validity phase.
- `PORT_0013 / spark` remains the generation-watchlist row and is excluded because it failed during execution.
- No final `GM_Speedup`, `RegressionRate`, or leaderboard can be claimed from this package.

## Outputs

- candidate matrix: `reports/evaluation/common_core_v0/direct_llm_timing_preflight/direct_llm_timing_candidate_matrix.csv`
- run plan: `reports/evaluation/common_core_v0/direct_llm_timing_preflight/direct_llm_timing_run_plan.json`
- future timing run directory: `reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_01/`

