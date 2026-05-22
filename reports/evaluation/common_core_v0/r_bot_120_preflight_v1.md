# R-Bot 120 Preflight v1

This file is a reviewable Stage-1 preflight scaffold for `R-Bot` on the
`common_core_v0_40_same_engine_120` rerun campaign.

It is preflight scaffolding only.

- No SQL generation was performed.
- No PostgreSQL, MySQL, or Spark execution was performed.
- No timing or speedup work was performed.
- No `R-Bot` generation command was executed.
- No result card or proposed row was created.

## Scope

- method_id: `r_bot`
- route_id: `r_bot_same_engine_rewrite`
- denominator_id: `common_core_v0_40_same_engine_120`
- planned rows: `120`
- engine scope under review: `pg`, `mysql`, `spark`

## Retained starting point

Retained artifacts show that `R-Bot` currently has bounded historical
PostgreSQL-oriented evidence plus bounded non-PG boundary evidence, not retained
tri-engine `120`-row same-engine evidence.

The key retained blockers are:

- retrieval corpus not recovered as a benchmark-ready retained substrate
- demo policy not closed with exact retrieval settings
- rule pool not recovered as a runnable formal route dependency
- contamination contract not yet attested in a formal run packet
- non-PG executable output contract not recovered
- no retained `120`-row generated-SQL output root populated by a run

The supporting retained artifacts used for this scaffold are:

- [common_core_v0_40_same_engine_120_rerun_manifest_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv)
- [common_core_v0_40_same_engine_120_route_contract_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_route_contract_v1.md)
- [method_role_freeze_for_rerun_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_role_freeze_for_rerun_v1.md)
- [failure_bucket_policy_for_rerun_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/failure_bucket_policy_for_rerun_v1.md)
- [prior_methods_common_core_v0_40_preflight.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/prior_methods_preflight/prior_methods_common_core_v0_40_preflight.md)
- [RBOT_LLMR2_READINESS_AUDIT_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/RBOT_LLMR2_READINESS_AUDIT_v0.md)
- [rbot_llmr2_retrieval_readiness_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/baseline_smoke/rbot_llmr2_retrieval_readiness_v0.json)
- [r_bot_upstream_runner_alignment_audit_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_upstream_runner_alignment_audit_v1.md)
- [r_bot_mysql_spark_feasibility_audit_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_mysql_spark_feasibility_audit_v1.md)
- [r_bot_same_engine_generation_01/README.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/r_bot_same_engine_generation_01/README.md)
- [r_bot_common_core_v0_40_same_engine_protocol.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_common_core_v0_40_same_engine_protocol.md)
- [r_bot_artifact_contract_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_artifact_contract_v1.md)
- [r_bot_formal_demo_policy_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/r_bot_formal_demo_policy_v1.md)
- [r_bot_formal_contamination_attestation_plan.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_substrate_freeze_01/r_bot_formal_contamination_attestation_plan.md)

## Current preflight interpretation

- `R-Bot` remains not aligned to the common `120`-row rerun target.
- Current PostgreSQL evidence is historical or bounded partial evidence only.
- MySQL and Spark executable support are not recovered from retained artifacts.
- A formal route contract exists on paper, but the executable route is still
  blocked by retrieval/demo/rule/output-contract dependencies.
- A same-engine generation package exists, but that package does not prove a
  closed tri-engine executable route.

The companion files created in this scaffold are:

- [r_bot_120_candidate_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_120_candidate_matrix_v1.csv)
- [r_bot_120_dependency_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_120_dependency_matrix_v1.csv)
- [r_bot_120_run_plan_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_120_run_plan_v1.json)

## Dependency snapshot

The dependency matrix marks the current route as blocked before generation.

High-severity blockers:

- retrieval corpus missing
- demo policy not closed
- rule pool missing
- contamination contract not attested
- per-engine SQL dialect support not recovered for executable MySQL/Spark paths
- reproducibility contract missing

Medium-severity blockers:

- input format contract is only partially recoverable from formal protocol notes
- output SQL contract is defined on paper but not satisfied by a retained full
  `120`-row run
- generated SQL retention path is planned but not satisfied by a retained run
- checker handoff is only partial historical PG evidence
- timing policy remains PG-subset-only historical evidence

## Next gate before execution

No Stage-2 generation work should begin until a human review confirms all of
the following:

1. retrieval corpus identity is frozen
2. demo policy is frozen with exact retrieval settings
3. rule pool and non-manual override path are frozen
4. contamination contract is attested
5. executable output SQL contract is closed for the route
6. generated SQL retention paths are defined for the future rerun
7. checker handoff is explicitly defined for future generated outputs
8. failure bucket policy is accepted for `R-Bot`

## Non-claims

- This scaffold does not claim `R-Bot` is runnable on
  `common_core_v0_40_same_engine_120`.
- This scaffold does not claim any `120`-row generation success.
- This scaffold does not claim any `120`-row execution success.
- This scaffold does not claim MySQL or Spark executable support.
- This scaffold does not update `method_comparison_summary_v2`.
