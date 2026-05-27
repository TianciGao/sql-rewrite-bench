# FORMAL_COMMON_CORE_FULL_METHOD_CONSISTENCY_SUMMARY_v0

## Status

Full 9-case common-core generated-method checker-backed consistency is now closed from existing report-local materialization and checker outputs.

This is generated-method checker-backed consistency only.

It is not admission.

It is not speedup scoring.

## Full 9-Case Denominator

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`
- `CONS_0007`
- `CONS_0012`

## SQLGlot Result

- route: `SQLGLOT_OPT_SAME_DIALECT`
- checker-backed consistency: `9 / 9`
- checker-backed inconsistency: `0 / 9`
- `result_consistency_rate=1.0`

## Direct LLM Result

- route: `LLM_DIRECT_REWRITE_STRONG`
- checker-backed consistency: `9 / 9`
- checker-backed inconsistency: `0 / 9`
- `result_consistency_rate=1.0`

## Checker Mode

- report-local generated-method checker mode: `exact_tsv_report_local`
- source and method results were materialized under `reports/formal_common_core/result_materialization/`
- generated-method checker outputs were written under `reports/formal_common_core/method_result_checks/`

## Report-Local Materialization Paths

- source TSVs:
  - `reports/formal_common_core/result_materialization/source/<case_id_lower>.tsv`
- SQLGlot TSVs:
  - `reports/formal_common_core/result_materialization/sqlglot_opt_same_dialect/<case_id_lower>.tsv`
- Direct LLM TSVs:
  - `reports/formal_common_core/result_materialization/llm_direct_rewrite/<case_id_lower>.tsv`
- SQLGlot checker outputs:
  - `reports/formal_common_core/method_result_checks/sqlglot_opt_same_dialect/<case_id_lower>.json`
- Direct LLM checker outputs:
  - `reports/formal_common_core/method_result_checks/llm_direct_rewrite/<case_id_lower>.json`

## Boundaries

- generated-method checker-backed consistency only
- not admission
- not speedup
- not leaderboard by itself
- no registry writeback
- no formal review update

