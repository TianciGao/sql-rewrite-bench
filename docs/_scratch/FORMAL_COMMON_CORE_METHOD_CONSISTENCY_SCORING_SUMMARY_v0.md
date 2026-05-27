# FORMAL_COMMON_CORE_METHOD_CONSISTENCY_SCORING_SUMMARY_v0

## 1. Status

This is a tracked scratch summary of the current formal common-core method consistency scoring state.

This summary covers:

- `SQLGLOT_OPT_SAME_DIALECT`
- `LLM_DIRECT_REWRITE_STRONG`

## 2. Input Reports

Primary command:

- `python -m scripts.cli formal-common-core-method-consistency-scoring`

Reports inspected:

- `reports/formal_common_core/native_identity_execution_v0.json`
- `reports/formal_common_core/control_scoring_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_execution_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_scoring_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_execution_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_scoring_v0.json`
- `reports/formal_common_core/control_execution_summary_v0.json`
- `reports/formal_common_core/method_consistency_scoring_v0.json`

## 3. SQLGlot Consistency Status

Current SQLGlot same-dialect method consistency status:

- row-count match: `9 / 9`
- `result_consistency_rate_status=not_computed_checker_required`
- `result_consistency_rate_observed_existing_artifacts=null`
- `formal_correctness_scoring_complete=false`

Current route interpretation:

- execution layer is complete
- row-count observation is complete
- checker-backed method consistency is still not computed

## 4. Direct LLM Consistency Status

Current Direct LLM rewrite method consistency status:

- row-count match: `9 / 9`
- `result_consistency_rate_status=not_computed_checker_required`
- `result_consistency_rate_observed_existing_artifacts=null`
- `formal_correctness_scoring_complete=false`

Current route interpretation:

- execution-layer formalization is complete from existing smoke artifacts
- row-count observation is complete
- checker-backed method consistency is still not computed

## 5. Row-Count Observations

Observed route-level row-count summary versus `NATIVE_IDENTITY`:

- SQLGlot same-dialect:
  - match `9 / 9`
  - mismatch `0 / 9`
  - unknown `0 / 9`
- Direct LLM rewrite:
  - match `9 / 9`
  - mismatch `0 / 9`
  - unknown `0 / 9`

## 6. Whether Checker-Backed Consistency Was Computed

Checker-backed consistency was not computed for either method route.

Current route-level status:

- `SQLGLOT_OPT_SAME_DIALECT`: `not_computed_checker_required`
- `LLM_DIRECT_REWRITE_STRONG`: `not_computed_checker_required`

## 7. Missing Artifact / Blocker Explanation

Existing checker artifacts are source / positive / negative witness artifacts.

They do not explicitly refer to:

- SQLGlot-generated candidate SQL
- Direct-LLM-generated candidate SQL
- a route-specific method-consistency judgment for these generated candidates

Because of that:

- row-count match remains only an execution observation
- method correctness cannot be promoted to checker-backed consistency from the current artifacts alone

## 8. Claim Boundaries

- row-count match is not semantic equivalence
- SQLGlot correctness should not be called `1.0`
- Direct LLM correctness should not be called `1.0`
- no speedup scoring has been done
- no leaderboard claim is available from this method snapshot

## 9. Recommended Next Action

- decide whether to create explicit route-specific result materialization and checker linkage for SQLGlot and Direct LLM, or formally freeze these routes at execution-plus-row-count-observation status for the first packet

## 10. Verification / Non-Modification Note

- only this note was created
- no database workloads were run
- no SQL was executed
- no SQLGlot was run
- no checker was run
- no LLM calls were made
- no registry changes were made
- `docs/EXECUTION_STATUS.md` was not changed
- no formal review files were changed
- taxonomy calibration notes were untouched
