# FORMAL_COMMON_CORE_METHOD_RESULT_MATERIALIZATION_PREFLIGHT_SUMMARY_v0

## 1. Status

This is a PERF-only, no-execution preflight for generated-route report-local result materialization.

It does not execute SQL.

It does not run checkers.

It does not create result TSVs or checker outputs.

## 2. PERF-only Denominator

- `PERF_0006`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`

Denominator case count: `7`

## 3. Routes Inspected

- `SQLGLOT_OPT_SAME_DIALECT`
- `LLM_DIRECT_REWRITE_STRONG`

## 4. Readiness Result

- checker config present: `7 / 7`
- source SQL present: `7 / 7`
- native execution success present: `7 / 7`
- SQLGlot candidate SQL available: `7 / 7`
- Direct LLM candidate SQL available: `7 / 7`
- SQLGlot ready for report-local materialization: `7 / 7`
- Direct LLM ready for report-local materialization: `7 / 7`
- overall `materialization_preflight_ready=true`
- `formal_method_consistency_currently_computable=false`

Interpretation:

- both generated routes are structurally ready for bounded PERF-only report-local result materialization
- checker-backed method consistency is still not computable because result materialization and route-specific checker outputs do not exist yet

## 5. Report-local Artifact Policy

Planned source result path:

- `reports/formal_common_core/result_materialization/source/<case_id_lower>.tsv`

Planned SQLGlot result path:

- `reports/formal_common_core/result_materialization/sqlglot_opt_same_dialect/<case_id_lower>.tsv`

Planned Direct LLM result path:

- `reports/formal_common_core/result_materialization/llm_direct_rewrite/<case_id_lower>.tsv`

Planned SQLGlot checker output path:

- `reports/formal_common_core/method_result_checks/sqlglot_opt_same_dialect/<case_id_lower>.json`

Planned Direct LLM checker output path:

- `reports/formal_common_core/method_result_checks/llm_direct_rewrite/<case_id_lower>.json`

These are policy paths only in this preflight. No TSV or checker file was created.

## 6. Current Blockers

Blocking counts for the PERF-only preflight are currently `0 / 7` for both generated routes.

Current non-readiness caveats:

- row-count match is not semantic equivalence
- source result TSVs are not materialized yet
- generated-method result TSVs are not materialized yet
- route-specific checker outputs are not materialized yet

## 7. Claim Boundaries

- no SQL executed
- no checker run
- no result materialization created
- no consistency scoring yet
- no speedup scoring
- no case-local writes

## 8. Recommended Next Action

- implement bounded PERF-only report-local result materialization and checker execution for SQLGlot and Direct LLM generated candidates
