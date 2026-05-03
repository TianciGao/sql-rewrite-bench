# FORMAL_COMMON_CORE_METHOD_PLAN_COLLECTION_SUMMARY_v0

## Status

This is a tracked scratch summary of bounded formal common-core method plan collection.

The collection scope was limited to PostgreSQL `EXPLAIN (FORMAT JSON)` over generated-method SQL read from existing formal reports.

Current batch status:

- SQLGlot same-dialect canary succeeded
- SQLGlot same-dialect 9-case plan collection succeeded
- Direct LLM rewrite 9-case plan collection succeeded
- `PERF_0024` required candidate-SQL source correction before the final rerun

## Command / Report References

Command:

- `python -m scripts.cli formal-common-core-method-plan-collection`

Primary report:

- `reports/formal_common_core/method_plan_collection_v0.json`

Plan outputs:

- `reports/formal_common_core/plans/sqlglot_opt_same_dialect/<case_id_lower>.json`
- `reports/formal_common_core/plans/llm_direct_rewrite/<case_id_lower>.json`

## SQLGlot Plan Collection Result

SQLGlot same-dialect completed successfully.

- route: `SQLGLOT_OPT_SAME_DIALECT`
- canary: `PERF_0006` succeeded
- 9-case collection: `9 / 9` succeeded
- plan JSON valid: `9 / 9`
- plan files written: `9 / 9`

## Direct LLM Plan Collection Result

Direct LLM rewrite completed successfully after candidate-SQL source correction.

- route: `LLM_DIRECT_REWRITE_STRONG`
- 9-case collection: `9 / 9` succeeded
- plan JSON valid: `9 / 9`
- plan files written: `9 / 9`

Observed correction detail for `PERF_0024`:

- the initial formal execution record carried a preview-truncated `extracted_sql_text`
- bounded plan collection now falls back to `baseline_call.extracted_sql_text` when the formal field is preview-contaminated
- final rerun succeeded with `EXPLAIN (FORMAT JSON)` only

## Plan Output Path Policy

Method plans are written only under report-local paths:

- SQLGlot:
  `reports/formal_common_core/plans/sqlglot_opt_same_dialect/<case_id_lower>.json`
- Direct LLM:
  `reports/formal_common_core/plans/llm_direct_rewrite/<case_id_lower>.json`

No generated SQL or plan artifact was written under `cases/`.

## Claim Boundaries

- EXPLAIN only
- no `EXPLAIN ANALYZE`
- no result execution
- no speedup scoring
- no attribution scoring
- no registry writeback
- no formal review update

## Next Action

- run plan observability post-collection preflight / parse summary over the completed SQLGlot and Direct LLM method-plan set
