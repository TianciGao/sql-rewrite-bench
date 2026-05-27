# FORMAL_COMMON_CORE_METHOD_PLAN_COLLECTION_PREFLIGHT_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of the current formal common-core method plan collection preflight state.

This is a readiness check for a later bounded EXPLAIN / plan-collection step.

## 2. Input Reports Inspected

Primary command:

- `python -m scripts.cli formal-common-core-method-plan-collection-preflight`

Reports inspected:

- `reports/formal_common_core/sqlglot_opt_same_dialect_execution_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_execution_v0.json`
- `reports/formal_common_core/plan_observability_preflight_v0.json`
- `reports/formal_common_core/control_exec_preflight_v0.json`
- `reports/formal_common_core/method_plan_collection_preflight_v0.json`

## 3. SQLGlot Generated SQL Readiness

Current SQLGlot readiness summary:

- `execution_report_present_count=9`
- `candidate_sql_available_count=9`
- `validation_schema_hint_count=9`
- `ready_for_future_plan_collection_count=9`
- `blocked_count=0`

Interpretation:

- SQLGlot generated candidate SQL is available for all 9 denominator cases from the formal SQLGlot execution report

## 4. Direct LLM Extracted SQL Readiness

Current Direct LLM readiness summary:

- `execution_report_present_count=9`
- `candidate_sql_available_count=9`
- `validation_schema_hint_count=9`
- `ready_for_future_plan_collection_count=9`
- `blocked_count=0`

Interpretation:

- Direct LLM extracted candidate SQL is available for all 9 denominator cases from the formal LLM execution report

## 5. Existing Method-Plan Artifact Status

Current existing method-plan artifact summary:

- SQLGlot existing method-plan artifacts:
  - `0 / 9`
- Direct LLM existing method-plan artifacts:
  - `0 / 9`

Interpretation:

- no method-specific plan artifacts currently exist under the planned report-local path

## 6. Future Plan-Output Path Policy

Future method-plan outputs should remain report-local and should not be written into `cases/`.

Planned future path policy:

- SQLGlot:
  - `reports/formal_common_core/plans/sqlglot_opt_same_dialect/<case_id_lower>.json`
- Direct LLM:
  - `reports/formal_common_core/plans/llm_direct_rewrite/<case_id_lower>.json`

This keeps method-plan collection separate from case-local control artifacts.

## 7. Speedup / Attribution Readiness

Current speedup / attribution readiness:

- `speedup_scoring_ready=false`

Interpretation:

- plans are not yet collected for generated methods
- no operator alignment or attribution has been computed
- no speedup has been computed

## 8. Missing Artifacts / Blockers

Current blockers are not candidate-SQL blockers.

Current blockers are:

- method-specific plan artifacts do not yet exist
- plan collection command has not yet been implemented for generated methods

The preflight shows that the later bounded collection step can proceed from formal reports without first writing generated SQL into `cases/`.

## 9. Claim Boundaries

- no EXPLAIN was run
- no SQL was executed
- no database connection was made
- no new plans were collected
- no generated SQL was written into `cases/`
- no operator alignment or attribution was computed
- no speedup was computed
- this only checks readiness for future bounded plan collection

## 10. Recommended Next Action

- implement bounded formal method plan collection for SQLGlot and Direct LLM using candidate SQL from formal reports and writing plans under `reports/formal_common_core/plans/`

## 11. Verification / Non-Modification Note

- only this note was created
- no database workloads were run
- no SQL was executed
- no EXPLAIN was run
- no SQLGlot was run
- no checker was run
- no LLM calls were made
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
