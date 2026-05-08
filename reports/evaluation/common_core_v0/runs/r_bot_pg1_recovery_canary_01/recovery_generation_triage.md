# Recovery Generation Triage

Run: `r_bot_pg1_recovery_canary_01`  
Scope: read-only artifact triage for the successful `R-Bot` PG1 exploratory generation canary  
Method boundary: no database run, no SQL execution, no LLM/API call, no package install

## Summary

- Planned rows: `1`
- Case: `PERF_0006`
- Exploratory generation outcome: `success`
- Current benchmark metric evidence: `false`
- Current claim boundary: `exploratory_smoke_only_not_current_common_core_metric_evidence`

## Triage Matrix

| Field | Value | Evidence |
|---|---|---|
| planned_rows | `1` | `run_results.json` |
| exploratory_generation_status | `exploratory_generation_success` | `run_results.json` |
| generated_sql_copied | `true` | `run_results.json` |
| output_sql_extracted | `true` | `run_results.json` / `smoke_actual.stdout.log` |
| generated_sql_path | `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated/PERF_0006/pg/r_bot_pg_rewrite.sql` | retained artifact |
| checker_candidate_sql_path | `reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/artifacts/PERF_0006_checker_candidate_sql.sql` | retained artifact |
| generated_sql_sql_only | `true` | retained SQL contains a single `SELECT` statement only |
| generated_sql_no_op_source_equivalent_by_normalized_text | `true` | normalized text matches [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PERF/PERF_0006/source.sql:1) and the retained checker candidate SQL |
| selected_rules_availability | `retained_present_but_available_false ; tmp_v3_visible_and_available_true` | retained `artifacts/PERF_0006_selected_rules.json`; visible `/tmp/.../selected_rules_v3.json` |
| retrieval_trace_availability | `retained_present_but_available_false ; tmp_v3_visible_and_available_true` | retained `artifacts/PERF_0006_retrieval_trace.json`; visible `/tmp/.../retrieval_trace_v3.json` |
| token_cost_log_availability | `retained_present_but_available_false ; tmp_v3_visible_and_available_true` | retained `artifacts/PERF_0006_token_cost_log.json`; visible `/tmp/.../token_cost_log_v3.json` |
| retrieval_vector_patch_status | `applied ; requested=true ; target_dim=100 ; actual_dim_not_observed` | `run_results.json` / `smoke_actual.stdout.log` |
| materialized_from_existing_actual | `true` | `run_results.json` |
| current_benchmark_metric_evidence | `false` | `run_results.json` |
| pg1_execution_validity_attemptable_as_exploratory_evidence | `conditional_future_human_run_only` | `r_bot_actual_run_gate_v1.md` allows only future human-run exploratory smoke; `run_results.json` still records `allow_actual_run=false` and `exploratory_actual_run_allowed=false` for the current package snapshot |

## Notes

- The retained generated SQL and retained checker candidate SQL are byte-for-byte identical in the inspected copies.
- The generated SQL is a no-op restatement of the frozen `PERF_0006` source query after normalization, not a substantive rewrite.
- The retained repo-side trace artifacts exist, but each retained JSON marks itself unavailable.
- The visible `/tmp` v3 artifacts show that selected-rules, retrieval-trace, and token/cost outputs were produced during the exploratory generation path.

## What Must Be Frozen Before This Can Become Current Benchmark Evidence

Per `r_bot_actual_run_gate_v1.md`, the following must be frozen or attested before any PG1 run can count as current benchmark evidence:

1. Smoke-scoped dependency environment documented and visible at run time.
2. Upstream clone identity pinned.
3. Retrieval corpus retained or frozen through an approved external artifact reference.
4. Index snapshot retained or frozen through an approved external artifact reference or deterministic rebuild contract.
5. Demo policy used by the actual run logged in retained artifacts.
6. Contamination exclusion policy attested in artifacts.
7. Full artifact contract satisfied, including retained generated SQL, selected-rules trace, retrieval trace, prompt text, raw model response, token/cost/provider metadata, environment snapshot, and package `run_results.json`.
8. Provider / model / base URL metadata logged without secrets.
9. Run results preserve explicit claim boundary and denominator identity.
