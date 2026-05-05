# LLMR2_10CASE_EXPANSION_PREFLIGHT_v1

## 0. Purpose And Boundary
This is no-execution preflight for LLM-R2 10-case expansion. It does not run LLM-R2, call any model/API, run Java rule application as a rewrite method, run any database, run checker, or run speedup.

## 1. Existing LLM-R2 Anchor
Bounded `PERF_0006` anchor:
- one-row fast path
- CPU-only
- schema-native contract
- output extraction cleanup
- checker consistent
- no speedup

## 2. Target Denominator
- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0052`
- `PERF_0054`
- `PERF_0063`

## 3. Per-case Readiness Table
| case_id | source_sql_exists | pg_schema_exists | pg_witness_exists | one_row_csv_ready | schema_native_json_ready | tiny_pool_ready | logical_plan_probe_ready_or_status | output_capture_contract_ready | checker_handoff_contract_ready | readiness_status | risk | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PERF_0006 | True | True | True | True | True | True | perf_0006_schema_native_probe_succeeded | True | True | ready_for_bounded_smoke | low | existing_perf_0006_anchor; bounded_fast_path_contract_staged |
| PERF_0008 | True | True | True | True | True | True | ready_to_run_preflight_only_probe_not_yet_run | True | True | ready_for_bounded_smoke | medium | leading_sql_comments_present; bounded_fast_path_contract_staged; logical_plan_probe_not_yet_run_for_this_case |
| PERF_0013 | True | True | True | True | True | True | ready_to_run_preflight_only_probe_not_yet_run | True | True | ready_for_bounded_smoke | medium | leading_sql_comments_present; bounded_fast_path_contract_staged; logical_plan_probe_not_yet_run_for_this_case |
| PERF_0017 | True | True | True | True | True | True | ready_to_run_preflight_only_probe_not_yet_run | True | True | ready_for_bounded_smoke | medium | leading_sql_comments_present; bounded_fast_path_contract_staged; logical_plan_probe_not_yet_run_for_this_case |
| PERF_0019 | True | True | True | True | True | True | ready_to_run_preflight_only_probe_not_yet_run | True | True | ready_for_bounded_smoke | medium | leading_sql_comments_present; bounded_fast_path_contract_staged; logical_plan_probe_not_yet_run_for_this_case |
| PERF_0024 | True | True | True | True | True | True | ready_to_run_preflight_only_probe_not_yet_run | True | True | ready_for_bounded_smoke | medium | leading_sql_comments_present; bounded_fast_path_contract_staged; logical_plan_probe_not_yet_run_for_this_case |
| PERF_0033 | True | True | True | True | True | True | ready_to_run_preflight_only_probe_not_yet_run | True | True | ready_for_bounded_smoke | medium | leading_sql_comments_present; bounded_fast_path_contract_staged; logical_plan_probe_not_yet_run_for_this_case |
| PERF_0052 | True | True | True | True | True | True | ready_to_run_preflight_only_probe_not_yet_run | True | True | ready_for_bounded_smoke | medium | leading_sql_comments_present; bounded_fast_path_contract_staged; logical_plan_probe_not_yet_run_for_this_case |
| PERF_0054 | True | True | True | True | True | True | ready_to_run_preflight_only_probe_not_yet_run | True | True | ready_for_bounded_smoke | medium | leading_sql_comments_present; bounded_fast_path_contract_staged; logical_plan_probe_not_yet_run_for_this_case |
| PERF_0063 | True | True | True | True | True | True | ready_to_run_preflight_only_probe_not_yet_run | True | True | ready_for_bounded_smoke | medium | leading_sql_comments_present; bounded_fast_path_contract_staged; logical_plan_probe_not_yet_run_for_this_case |

## 4. Recommended Execution Batches
- Batch A:
  - `PERF_0008`
  - `PERF_0013`
  - `PERF_0017`
- Batch B:
  - `PERF_0019`
  - `PERF_0024`
  - `PERF_0033`
- Batch C:
  - `PERF_0052`
  - `PERF_0054`
  - `PERF_0063`

## 5. Metrics To Report Later
- `candidate_generation_rate@10`
- `executable_rate@10`
- `result_consistency_rate@10`
- `output_extraction_failure_count`
- `logical_plan_failure_count`
- `checker_failed_count`
- `speedup_status = not_run`

Do not compute:
- `gm_speedup`
- `regression_rate@20`
- leaderboard rank

## 6. Claim Boundary
- `bounded_10case_LLMR2_smoke_subset_not_leaderboard`

## 7. Recommended Next Step
- `execute LLM-R2 Batch A`

## 8. Non-Modification Note
Confirm no execution/model/API/DB/checker/speedup and no case/registry/review/rules/EXECUTION_STATUS changes.
