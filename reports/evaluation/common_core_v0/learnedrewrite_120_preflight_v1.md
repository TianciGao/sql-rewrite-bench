# LearnedRewrite 120 Preflight v1

This file is a reviewable Stage-1 preflight scaffold for `LearnedRewrite` on the
`common_core_v0_40_same_engine_120` rerun campaign.

It is preflight scaffolding only.

- No SQL generation was performed.
- No PostgreSQL, MySQL, or Spark execution was performed.
- No timing or speedup work was performed.
- No `LearnedRewrite` inference was executed.
- No result card or proposed row was created.

## Scope

- method_id: `learnedrewrite`
- route_id: `learnedrewrite_same_engine_120_preflight`
- denominator_id: `common_core_v0_40_same_engine_120`
- planned rows: `120`
- engine scope under review: `pg`, `mysql`, `spark`

## Retained starting point

Retained artifacts show that `LearnedRewrite` currently has bounded historical
PG-only evidence on `prior_method_pg10`, not retained `120`-row same-engine
evidence.

The key retained blockers are:

- adapter not recovered
- checkpoint not recovered
- inference entrypoint not recovered
- no retained `120`-row generated-SQL path
- no retained MySQL evidence
- no retained Spark evidence

The supporting retained artifacts used for this scaffold are:

- [common_core_v0_40_same_engine_120_rerun_manifest_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv)
- [common_core_v0_40_same_engine_120_route_contract_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_route_contract_v1.md)
- [method_role_freeze_for_rerun_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_role_freeze_for_rerun_v1.md)
- [failure_bucket_policy_for_rerun_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/failure_bucket_policy_for_rerun_v1.md)
- [prior_methods_common_core_v0_40_preflight.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/prior_methods_preflight/prior_methods_common_core_v0_40_preflight.md)
- [LEARNED_REWRITE_READINESS_AUDIT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/LEARNED_REWRITE_READINESS_AUDIT_v0.md)
- [learnedrewrite_input_readiness_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/baseline_smoke/learnedrewrite_input_readiness_v0.json)

## Current preflight interpretation

- `LearnedRewrite` remains not aligned to the common `120`-row rerun target.
- Historical `prior_method_pg10` evidence remains bounded prior-method evidence
  only.
- MySQL and Spark support are not recovered from retained artifacts.
- PostgreSQL support is only retained as bounded historical evidence and is not
  a current `120`-row execution-ready route.

The companion files created in this scaffold are:

- [learnedrewrite_120_candidate_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/learnedrewrite_120_candidate_matrix_v1.csv)
- [learnedrewrite_120_dependency_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/learnedrewrite_120_dependency_matrix_v1.csv)
- [learnedrewrite_120_run_plan_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/learnedrewrite_120_run_plan_v1.json)

## Dependency snapshot

The dependency matrix marks the current route as blocked before generation.

High-severity blockers:

- adapter missing
- checkpoint missing
- inference entrypoint missing
- generated SQL retention path for a common-core `120` rerun not established
- per-engine SQL dialect support not recovered for MySQL or Spark

Medium-severity blockers:

- input format contract is only partially recoverable from readiness notes
- output SQL extraction path is not recovered as a retained common-core route
- checker handoff is only bounded historical PG-only evidence
- timing policy remains unresolved for any later `120` route

## Next gate before execution

No Stage-2 generation work should begin until a human review confirms all of
the following:

1. adapter, checkpoint, and inference entrypoint are recovered
2. engine coverage is explicitly frozen for `pg`, `mysql`, and `spark`
3. generated SQL retention paths are defined for the future rerun
4. checker handoff is explicitly defined for future generated outputs
5. failure bucket policy is accepted for `LearnedRewrite`

## Non-claims

- This scaffold does not claim `LearnedRewrite` is runnable on
  `common_core_v0_40_same_engine_120`.
- This scaffold does not claim any `120`-row generation success.
- This scaffold does not claim any `120`-row execution success.
- This scaffold does not claim MySQL or Spark support.
- This scaffold does not update `method_comparison_summary_v2`.
