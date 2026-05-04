# FORMAL_COMMON_CORE_METHOD_RESULT_CHECKER_RUN_SUMMARY_v0

## Status

PERF-only report-local result materialization and checker execution completed for both generated routes.

This run used report-local TSV materialization under `reports/formal_common_core/`.

It did not write into `cases/`.

## PERF-only Scope

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`

## SQLGlot Checker-backed Consistency Result

- route: `SQLGLOT_OPT_SAME_DIALECT`
- materialized cases: `7 / 7`
- checker success: `7 / 7`
- checker consistent: `7`
- checker inconsistent: `0`
- checker unavailable: `0`
- `result_consistency_rate=1.0`
- `result_consistency_rate_status=computed_from_report_local_exact_tsv`

## Direct LLM Checker-backed Consistency Result

- route: `LLM_DIRECT_REWRITE_STRONG`
- materialized cases: `7 / 7`
- checker success: `7 / 7`
- checker consistent: `7`
- checker inconsistent: `0`
- checker unavailable: `0`
- `result_consistency_rate=1.0`
- `result_consistency_rate_status=computed_from_report_local_exact_tsv`

## Report-local Artifact Paths

Source TSVs:

- `reports/formal_common_core/result_materialization/source/<case_id_lower>.tsv`

SQLGlot TSVs:

- `reports/formal_common_core/result_materialization/sqlglot_opt_same_dialect/<case_id_lower>.tsv`

Direct LLM TSVs:

- `reports/formal_common_core/result_materialization/llm_direct_rewrite/<case_id_lower>.tsv`

SQLGlot checker outputs:

- `reports/formal_common_core/method_result_checks/sqlglot_opt_same_dialect/<case_id_lower>.json`

Direct LLM checker outputs:

- `reports/formal_common_core/method_result_checks/llm_direct_rewrite/<case_id_lower>.json`

## Inconsistent Cases

- none in the PERF-only denominator for either generated route

## Checker Mode

- `exact_tsv_report_local`

Interpretation:

- this is checker-backed consistency from report-local result materialization
- it is stronger than row-count-only observation
- it is still PERF-only, not full 9-case common-core closure

## Boundaries

- PERF-only
- report-local materialization only
- not CONS
- not speedup
- not PORT
- not full leaderboard
- row-count match alone is not semantic equivalence

## Recommended Next Action

- decide whether to extend bounded report-local result materialization and checker execution to the remaining CONS cases, or keep generated-method checker-backed consistency as PERF-only for the current packet
