# FORMAL_COMMON_CORE_METHOD_RESULT_CHECKER_PREFLIGHT_SUMMARY_v0

## 1. Status

This is the formal common-core method result-checker preflight summary for generated routes.

It is preflight only.

It does not execute SQL.

It does not run checkers.

## 2. Inputs Inspected

- `reports/formal_common_core/native_identity_execution_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_execution_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_execution_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_scoring_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_scoring_v0.json`
- `reports/formal_common_core/method_consistency_scoring_v0.json`
- `reports/formal_common_core/control_scoring_v0.json`
- `cases/<POOL>/<CASE>/validation/checker.yaml` where present
- `cases/<POOL>/<CASE>/runs/pg/result_check.json` where present
- `cases/<POOL>/<CASE>/runs/result_check.json` where present
- `reports/formal_common_core/method_result_checker_preflight_v0.json`

## 3. SQLGlot Method Checker Readiness

- candidate SQL available: `9 / 9`
- existing route-specific method checker artifacts: `0 / 9`
- ready from existing route-specific checker artifacts: `0 / 9`
- ready for future report-local result materialization: `7 / 9`
- blocked by missing checker config: `2 / 9`

Interpretation:

- SQLGlot same-dialect already has enough candidate SQL and execution evidence for a future report-local checker flow
- there are no existing SQLGlot-specific checker outputs yet
- `CONS_0007` and `CONS_0012` are blocked because case-local `checker.yaml` is missing

## 4. Direct LLM Method Checker Readiness

- candidate SQL available: `9 / 9`
- existing route-specific method checker artifacts: `0 / 9`
- ready from existing route-specific checker artifacts: `0 / 9`
- ready for future report-local result materialization: `7 / 9`
- blocked by missing checker config: `2 / 9`

Interpretation:

- Direct LLM rewrite also has enough candidate SQL and execution evidence for a future report-local checker flow
- there are no existing Direct-LLM-specific checker outputs yet
- `CONS_0007` and `CONS_0012` are blocked because case-local `checker.yaml` is missing

## 5. Why Current Checker-Backed Method Consistency Is Not Yet Claimable

- existing case-local `result_check.json` artifacts are source / witness artifacts, not generated-method checker artifacts
- no route-specific method result materialization exists yet under report-local paths
- no route-specific method checker outputs exist yet under report-local paths
- row-count match remains observation only
- current `formal_method_consistency_currently_computable=false`

## 6. Future Report-Local Artifact Policy

Do not write into `cases/`.

Future report-local result materialization and checker outputs should use:

- `reports/formal_common_core/result_materialization/source/<case_id_lower>.tsv`
- `reports/formal_common_core/result_materialization/sqlglot_opt_same_dialect/<case_id_lower>.tsv`
- `reports/formal_common_core/result_materialization/llm_direct_rewrite/<case_id_lower>.tsv`
- `reports/formal_common_core/method_result_checks/sqlglot_opt_same_dialect/<case_id_lower>.json`
- `reports/formal_common_core/method_result_checks/llm_direct_rewrite/<case_id_lower>.json`

## 7. What Can Be Done Next

- PERF cases are ready for a bounded report-local result materialization design
- generated-route checker-backed consistency remains blocked until result materialization and method checker outputs exist
- CONS cases need an explicit checker-config decision before they can join the same route-specific checker flow

## 8. Claim Boundaries

- no SQL execution
- no checker execution
- no consistency scoring
- row-count match is not semantic equivalence
- existing witness result-check artifacts must not be re-labeled as SQLGlot or Direct LLM method checker artifacts

## 9. Recommended Next Action

- implement bounded report-local result materialization preflight for SQLGlot and Direct LLM generated candidates, without writing into `cases/`
