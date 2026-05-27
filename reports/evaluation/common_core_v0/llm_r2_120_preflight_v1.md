# LLM-R2 120 Preflight v1

This file is a reviewable Stage-1 preflight scaffold for `LLM-R2` on the
`common_core_v0_40_same_engine_120` rerun campaign.

It is preflight scaffolding only.

- No SQL generation was performed.
- No PostgreSQL, MySQL, or Spark execution was performed.
- No timing or speedup work was performed.
- No `LLM-R2` inference was executed.
- No result card or proposed row was created.

## Scope

- method_id: `llm_r2`
- route_id: `llm_r2_same_engine_120_preflight`
- denominator_id: `common_core_v0_40_same_engine_120`
- planned rows: `120`
- engine scope under review: `pg`, `mysql`, `spark`

## Retained starting point

Retained artifacts show that `LLM-R2` currently has bounded historical PG-only
evidence on `prior_method_pg10`, not retained `120`-row same-engine evidence.

The key retained blockers are:

- reusable runner not recovered for a common-core `120` route
- logical-plan substrate not closed as a repeatable common-core route
- output SQL extraction is only bounded one-case cleanup evidence
- no retained `120`-row generated-SQL path
- no retained MySQL evidence
- no retained Spark evidence

The supporting retained artifacts used for this scaffold are:

- [common_core_v0_40_same_engine_120_rerun_manifest_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv)
- [common_core_v0_40_same_engine_120_route_contract_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_route_contract_v1.md)
- [method_role_freeze_for_rerun_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_role_freeze_for_rerun_v1.md)
- [failure_bucket_policy_for_rerun_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/failure_bucket_policy_for_rerun_v1.md)
- [prior_methods_common_core_v0_40_preflight.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/prior_methods_preflight/prior_methods_common_core_v0_40_preflight.md)
- [RBOT_LLMR2_READINESS_AUDIT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/RBOT_LLMR2_READINESS_AUDIT_v0.md)
- [rbot_llmr2_retrieval_readiness_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/baseline_smoke/rbot_llmr2_retrieval_readiness_v0.json)
- [LLMR2_10CASE_SMOKE_ROLLUP_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_10CASE_SMOKE_ROLLUP_v1.md)
- [LLMR2_EXTERNAL_REPO_SUBSTRATE_AUDIT_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_EXTERNAL_REPO_SUBSTRATE_AUDIT_v1.md)
- [LLMR2_OUTPUT_SQL_EXTRACTION_AUDIT_PERF_0006_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_OUTPUT_SQL_EXTRACTION_AUDIT_PERF_0006_v1.md)
- [LLMR2_LOGICAL_PLAN_FAILURE_AUDIT_PERF_0006_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LLMR2_LOGICAL_PLAN_FAILURE_AUDIT_PERF_0006_v1.md)
- [PRIOR_METHOD_SPEEDUP_LLMR2_BATCH_B_v1.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/PRIOR_METHOD_SPEEDUP_LLMR2_BATCH_B_v1.md)

## Current preflight interpretation

- `LLM-R2` remains not aligned to the common `120`-row rerun target.
- Historical `prior_method_pg10` evidence remains bounded prior-method evidence
  only.
- MySQL and Spark support are not recovered from retained artifacts.
- PostgreSQL support is only retained as bounded historical evidence and is not
  a current `120`-row execution-ready route.
- One-case extraction cleanup evidence does not yet establish a reusable
  extraction contract for a common-core `120` rerun.

The companion files created in this scaffold are:

- [llm_r2_120_candidate_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_candidate_matrix_v1.csv)
- [llm_r2_120_dependency_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_dependency_matrix_v1.csv)
- [llm_r2_120_run_plan_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_run_plan_v1.json)

## Dependency snapshot

The dependency matrix marks the current route as blocked before generation.

High-severity blockers:

- runner missing
- logical-plan substrate not closed
- per-engine SQL dialect support not recovered for MySQL or Spark
- generated SQL retention path for a common-core `120` rerun not established
- reproducibility contract for demo/rule-selection flow not frozen

Medium-severity blockers:

- output SQL extraction is only partially evidenced on a one-case cleanup path
- input format contract is only partially recoverable from substrate notes
- checker handoff is only bounded historical PG-only evidence
- timing policy remains unresolved for any later `120` route

## Next gate before execution

No Stage-2 generation work should begin until a human review confirms all of
the following:

1. reusable runner path is recovered
2. logical-plan substrate is repeatable for rerun inputs
3. output SQL extraction is frozen as a reusable route contract
4. engine coverage is explicitly frozen for `pg`, `mysql`, and `spark`
5. generated SQL retention paths are defined for the future rerun
6. checker handoff is explicitly defined for future generated outputs
7. failure bucket policy is accepted for `LLM-R2`

## Non-claims

- This scaffold does not claim `LLM-R2` is runnable on
  `common_core_v0_40_same_engine_120`.
- This scaffold does not claim any `120`-row generation success.
- This scaffold does not claim any `120`-row execution success.
- This scaffold does not claim MySQL or Spark support.
- This scaffold does not update `method_comparison_summary_v2`.
