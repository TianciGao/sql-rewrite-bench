# Paper Results Index for common_core_v0

This is the first file to read when writing the paper results section.

It is the stable entry point for the paper-facing result artifacts under
`reports/evaluation/common_core_v0/`. Future result summaries should be linked
from this file rather than left isolated.

## Canonical Paper-Facing Tables

- Denominator-aware evidence ledger:
  - [method_comparison_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.md)
- Safety / readiness check for the canonical ledger:
  - [method_comparison_summary_v2_paper_readiness_check_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2_paper_readiness_check_v2.md)
- Reviewable draft row-admission policy for future paper-table governance:
  - [paper_table_row_admission_policy_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/paper_table_row_admission_policy_v1.md)

## Governance Boundary

- Fixed first-read evidence freeze folder now exists:
  - [00_PAPER_EVIDENCE_FREEZE_V1/README.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/README.md)
  - [00_PAPER_EVIDENCE_FREEZE_V1/METHOD_STATUS_LEDGER.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/METHOD_STATUS_LEDGER.csv)
  - [00_PAPER_EVIDENCE_FREEZE_V1/ARTIFACT_INDEX.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/ARTIFACT_INDEX.csv)
  - [00_PAPER_EVIDENCE_FREEZE_V1/RERUN_CAMPAIGN_LEDGER.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/RERUN_CAMPAIGN_LEDGER.csv)
  - [00_PAPER_EVIDENCE_FREEZE_V1/DECISION_NOTES.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/DECISION_NOTES.md)
  - [00_PAPER_EVIDENCE_FREEZE_V1/NEXT_ACTIONS.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/NEXT_ACTIONS.md)
  - [00_PAPER_EVIDENCE_FREEZE_V1/RECOVERY_PRIORITY_DECISION_V1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/RECOVERY_PRIORITY_DECISION_V1.md)
- R-Bot common-core `120` evidence reconciliation packet now also exists:
  - [r_bot_common_core_120_evidence_reconciliation_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.md)
  - [r_bot_common_core_120_evidence_reconciliation_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.csv)
- Future ChatGPT and Codex sessions should read this freeze folder first before
  proposing new Common-core v0 paper-results or `120`-rerun work.
- [paper_table_row_admission_policy_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/paper_table_row_admission_policy_v1.md)
  is a reviewable policy draft only.
- It does not update `method_comparison_summary_v2`.
- It does not create a leaderboard.
- It does not promote any proposed row into canonical status.
- Reviewable Stage-0 rerun-campaign governance drafts now also exist:
  - [common_core_v0_40_same_engine_120_route_contract_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_route_contract_v1.md)
  - [method_role_freeze_for_rerun_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_role_freeze_for_rerun_v1.md)
  - [failure_bucket_policy_for_rerun_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/failure_bucket_policy_for_rerun_v1.md)
  - [common_core_v0_40_same_engine_120_rerun_manifest_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv)
- These rerun drafts are planning-only.
- They do not authorize execution.
- They do not create result cards or proposed rows.
- A reviewable Stage-1 LearnedRewrite preflight scaffold now also exists:
  - [learnedrewrite_120_preflight_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/learnedrewrite_120_preflight_v1.md)
  - [learnedrewrite_120_candidate_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/learnedrewrite_120_candidate_matrix_v1.csv)
  - [learnedrewrite_120_dependency_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/learnedrewrite_120_dependency_matrix_v1.csv)
  - [learnedrewrite_120_run_plan_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/learnedrewrite_120_run_plan_v1.json)
- This LearnedRewrite packet is preflight scaffolding only.
- It does not claim generation support, execution support, or `120`-row evidence.
- A reviewable Stage-1 LLM-R2 preflight scaffold now also exists:
  - [llm_r2_120_preflight_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_preflight_v1.md)
  - [llm_r2_120_candidate_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_candidate_matrix_v1.csv)
  - [llm_r2_120_dependency_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_dependency_matrix_v1.csv)
  - [llm_r2_120_run_plan_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_run_plan_v1.json)
- A reviewable LLM-R2 recovery plan now also exists:
  - [llm_r2_120_recovery_plan_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_recovery_plan_v1.md)
  - [llm_r2_120_recovery_plan_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_recovery_plan_v1.csv)
  - [llm_r2_120_recovery_checklist_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_recovery_checklist_v1.md)
- A reviewable LLM-R2 runner recovery scaffold now also exists:
  - [llm_r2_120_runner_recovery_scaffold_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_runner_recovery_scaffold_v1.md)
  - [llm_r2_120_runner_recovery_scaffold_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_runner_recovery_scaffold_v1.csv)
  - [llm_r2_120_runner_dry_run_validator_v1.py](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_runner_dry_run_validator_v1.py)
  - [llm_r2_120_runner_recovery_inventory_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_120_runner_recovery_inventory_v1.json)
- A reviewable LLM-R2 bounded PostgreSQL overlap dry-run plan now also exists:
  - [llm_r2_bounded_pg_overlap_dry_run_plan_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_dry_run_plan_v1.md)
  - [llm_r2_bounded_pg_overlap_dry_run_plan_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_dry_run_plan_v1.csv)
  - [llm_r2_bounded_pg_overlap_candidate_slice_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_candidate_slice_v1.csv)
  - [llm_r2_bounded_pg_overlap_approval_gate_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_approval_gate_v1.md)
- A reviewable LLM-R2 bounded PostgreSQL overlap execution runbook now also exists:
  - [llm_r2_bounded_pg_overlap_execution_runbook_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_execution_runbook_v1.md)
  - [llm_r2_bounded_pg_overlap_command_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_command_matrix_v1.csv)
  - [llm_r2_bounded_pg_overlap_expected_artifacts_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_expected_artifacts_v1.csv)
  - [llm_r2_bounded_pg_overlap_failure_bucket_mapping_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_failure_bucket_mapping_v1.csv)
- A reviewable LLM-R2 bounded PostgreSQL overlap human-run approval record and packet now also exist:
  - [llm_r2_bounded_pg_overlap_human_run_approval_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_human_run_approval_v1.md)
  - [llm_r2_bounded_pg_overlap_human_run_approval_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_human_run_approval_v1.csv)
  - [llm_r2_bounded_pg_overlap_human_run_packet_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_bounded_pg_overlap_human_run_packet_v1.md)
- A reviewable LLM-R2 slice-to-runner compatibility packet now also exists:
  - [llm_r2_slice_to_runner_compatibility_addendum_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_slice_to_runner_compatibility_addendum_v1.md)
  - [llm_r2_slice_to_runner_compatibility_addendum_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_slice_to_runner_compatibility_addendum_v1.csv)
  - [llm_r2_supported_pg3_candidate_slice_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_candidate_slice_v1.csv)
  - [llm_r2_unsupported_pg5_wrapper_extension_plan_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_unsupported_pg5_wrapper_extension_plan_v1.md)
- A completed LLM-R2 supported PG3 generation dry-run governance review now
  also exists:
  - [llm_r2_supported_pg3_generation_dry_run_review_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_generation_dry_run_review_v1.md)
  - [llm_r2_supported_pg3_generation_dry_run_review_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_generation_dry_run_review_v1.csv)
  - retained run directory:
    [runs/llm_r2_supported_pg3_generation_dry_run_01](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/runs/llm_r2_supported_pg3_generation_dry_run_01)
- This LLM-R2 packet is preflight scaffolding only.
- It does not claim `120`-row evidence, and the original 8-row approval is now
  superseded by runner-compatibility review. Only a 3-row PG subset is
  currently runner-supported, pending separate human reapproval.
- The completed PG3 local human-run packet is generation-only dry-run evidence
  under governance review, not PostgreSQL execution, checker, timing, speedup,
  MySQL/Spark, or full `120` evidence.
- A reviewable Stage-1 R-Bot preflight scaffold now also exists:
  - [r_bot_120_preflight_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_120_preflight_v1.md)
  - [r_bot_120_candidate_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_120_candidate_matrix_v1.csv)
  - [r_bot_120_dependency_matrix_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_120_dependency_matrix_v1.csv)
  - [r_bot_120_run_plan_v1.json](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_120_run_plan_v1.json)
- This R-Bot packet is preflight scaffolding only.
- It does not claim generation support, execution support, or `120`-row evidence.
- A reviewable LLM-R2 supported PG3 static SQL inspection packet now also
  exists:
  - [llm_r2_supported_pg3_static_sql_inspection_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_static_sql_inspection_v1.md)
  - [llm_r2_supported_pg3_static_sql_inspection_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_static_sql_inspection_v1.csv)
- This LLM-R2 PG3 packet is static inspection only.
- It does not authorize PostgreSQL execution, checker, timing, or speedup.
- It does not create paper evidence or `120`-row evidence.
- A reviewable LLM-R2 supported PG3 PostgreSQL execution/checker planning
  packet now also exists:
  - [llm_r2_supported_pg3_pg_execution_checker_plan_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_pg_execution_checker_plan_v1.md)
  - [llm_r2_supported_pg3_pg_execution_checker_plan_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_pg_execution_checker_plan_v1.csv)
  - [llm_r2_supported_pg3_pg_execution_checker_approval_gate_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_pg_execution_checker_approval_gate_v1.md)
- This LLM-R2 PG3 packet is planning only.
- It does not authorize PostgreSQL execution, checker, timing, or speedup.
- It does not create correctness, exact-match, or `120`-row evidence.
- A reviewable LLM-R2 supported PG3 PostgreSQL execution input recovery packet
  now also exists:
  - [llm_r2_supported_pg3_pg_execution_input_recovery_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_pg_execution_input_recovery_v1.md)
  - [llm_r2_supported_pg3_pg_execution_input_recovery_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_pg_execution_input_recovery_v1.csv)
- This LLM-R2 PG3 packet is read-only path recovery only.
- It does not authorize PostgreSQL execution, checker, timing, or speedup.
- It does not create correctness, exact-match, or `120`-row evidence.
- A completed LLM-R2 supported PG3 PostgreSQL execution/checker governance
  review packet now also exists:
  - [llm_r2_supported_pg3_pg_execution_checker_review_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_pg_execution_checker_review_v1.md)
  - [llm_r2_supported_pg3_pg_execution_checker_review_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/llm_r2_supported_pg3_pg_execution_checker_review_v1.csv)
- This LLM-R2 PG3 packet is governance review of a completed local human-run.
- It is PG3-only and not PG40 or full `120` evidence.
- It is not MySQL/Spark evidence and not timing/speedup evidence.

## Method Summary Files

### SQLGlot

- [sqlglot_validity_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_validity_summary_v1.md)
- [sqlglot_speedup_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_speedup_summary_v1.md)
- [sqlglot_paper_route_audit_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_paper_route_audit_v1.md)
- [sqlglot_optimize_same_dialect_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_optimize_same_dialect_result_card_v1.md)
- [sqlglot_optimize_same_dialect_proposed_row_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_optimize_same_dialect_proposed_row_v1.md)
- [sqlglot_transpile_same_dialect_noop_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_transpile_same_dialect_noop_result_card_v1.md)
- [sqlglot_method_comparison_proposed_row_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_method_comparison_proposed_row_v1.md)

### Direct LLM

- [direct_llm_validity_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_validity_summary_v1.md)
- [direct_llm_speedup_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_speedup_summary_v1.md)
- [direct_llm_same_engine_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_same_engine_result_card_v1.md)
- [direct_llm_same_engine_proposed_row_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/direct_llm_same_engine_proposed_row_v1.md)

### Bounded Prior-Method Appendix

- [prior_methods_pg10_bounded_appendix_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md)
  packages retained `prior_method_pg10` PG-only appendix evidence for
  `LearnedRewrite` and `LLM-R2`.
- This appendix is bounded prior-method evidence only.
- It is not `common_core_v0_40_same_engine_120` evidence.
- It does not update `method_comparison_summary_v2`.
- It does not promote `LearnedRewrite` or `LLM-R2` into the main same-engine
  method evidence table.

### Calcite HEP

- [calcite_hep_validity_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_validity_summary_v1.md)
- [calcite_hep_speedup_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_speedup_summary_v1.md)
- Bounded MySQL/Spark canary boundary card:
  - [calcite_hep_mysql_spark_canary_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_mysql_spark_canary_result_card_v1.md)
- Bounded MySQL/Spark execution-expansion result card:
  - [calcite_hep_mysql_spark_execution_expansion_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_mysql_spark_execution_expansion_result_card_v1.md)
- Fail-closed `120`-row synthesis, bounded recovery canary result card, and proposed paper row:
  - [calcite_hep_120_fail_closed_synthesis_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_fail_closed_synthesis_v1.md)
  - [calcite_hep_120_post93_frontier_audit_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_post93_frontier_audit_v1.md)
  - [calcite_hep_120_recovery_canary_08_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_recovery_canary_08_result_card_v1.md)
  - [calcite_hep_120_recovery_round2_canary_09_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_recovery_round2_canary_09_result_card_v1.md)
  - [calcite_hep_120_recovery_round4b_numeric_scale_canary_04_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_recovery_round4b_numeric_scale_canary_04_result_card_v1.md)
  - [calcite_hep_120_recovery_perf0035_canary_03_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_recovery_perf0035_canary_03_result_card_v1.md)
  - [calcite_hep_method_comparison_proposed_row_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_method_comparison_proposed_row_v1.md)

### R-Bot

- Canonical current PostgreSQL paper-facing evidence:
  - [r_bot_pg_expansion_result_card_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_pg_expansion_result_card_v2.md)
  - [r_bot_pg15_speedup_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_pg15_speedup_summary_v2.md)
- Historical retained PG7 evidence:
  - [r_bot_formal_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_formal_result_card_v1.md)
  - [r_bot_pg7_speedup_summary_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_pg7_speedup_summary_v1.md)
- MySQL/Spark boundary evidence:
  - [r_bot_mysql_spark_canary_result_card_v1.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_mysql_spark_canary_result_card_v1.md)

## SQLGlot Current Paper-Safe Status

- SQLGlot retains two same-engine route-level rows:
  - `sqlglot_optimize_same_dialect`
  - `sqlglot_transpile_same_dialect_noop`
- The next promoted paper-facing SQLGlot route is:
  - `sqlglot_transpile_same_dialect_noop`
  - denominator `common_core_v0_40_same_engine_120_transpile_noop_route`
  - generated `78 / 120`
  - executed `72 / 120`
  - match_exact `72 / 120`
  - exact among executed `72 / 72`
  - timing only on `timing_success_72_on_transpile_noop_route`
- A second retained paper-facing SQLGlot route is:
  - `sqlglot_optimize_same_dialect`
  - denominator `common_core_v0_40_same_engine_120_optimize_route`
  - generated `75 / 120`
  - executed `65 / 120`
  - match_exact `65 / 120`
  - exact among executed `65 / 65`
  - timing only on `timing_success_65_on_optimize_route`
- This is denominator-aware route evidence, not cross-dialect portability
  evidence, not a full SQLGlot method-family aggregate, and not
  leaderboard-comparable evidence.

## R-Bot Current Paper-Safe Status

- R-Bot PG evidence is represented by PG expansion v2.
- R-Bot MySQL/Spark canary reached generation attempts but generated `0 / 6`
  executable SQL outputs.
- MySQL/Spark for R-Bot remain `NA_not_computed`, not `correctness = 0`.
- R-Bot is `pg_only` in
  [method_comparison_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.md).

## Calcite HEP Current Paper-Safe Status

- The canonical Calcite HEP row in
  [method_comparison_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.md)
  remains `pg_only`.
- A bounded MySQL/Spark canary now exists:
  - `6 / 6` rewrite success
  - `6 / 6` executed
  - `4 / 6` match_exact
  - `2 / 6` mismatch due to aggregate decimal scale loss
- A bounded MySQL/Spark non-PG expansion now exists:
  - `80` attempted rewrite rows
  - `60` rewrite_success
  - `60` execution-planned rows
  - `59` executed
  - `49` match_exact
  - `10` mismatch
  - `1` Spark setup artifact
- A denominator-aware fail-closed `120`-row synthesis now exists and has been updated after the bounded recovery canary:
  - retained PG evidence now contributes `31 / 40` exact matches
  - retained non-PG evidence now contributes `62 / 80` exact matches
  - combined fail-closed exact-match ledger improved from `70 / 120` to `93 / 120`
  - the recovery canary added `5` recovered exact rows: `PERF_0008:mysql`, `PERF_0013:mysql`, `PERF_0017:mysql`, `PERF_0019:mysql`, `PERF_0077:spark`
  - the round-2 recovery canary added `5` more recovered exact rows: `LONGTAIL_0022:pg`, `LONGTAIL_0023:pg`, `LONGTAIL_0024:pg`, `LONGTAIL_0012:mysql`, `LONGTAIL_0012:spark`
  - the round-3 and round-3c recovery chain added `6` more recovered exact rows: `CONS_0036:pg`, `CONS_0037:pg`, `LONGTAIL_0011:pg`, `LONGTAIL_0012:pg`, `PERF_0062:mysql`, `LONGTAIL_0013:mysql`
  - the round-4b numeric-scale recovery canary added `4` more recovered exact rows: `PERF_0062:pg`, `PERF_0062:spark`, `LONGTAIL_0013:pg`, `LONGTAIL_0013:spark`
  - the bounded `PERF_0035` recovery canary added `3` more recovered exact rows: `PERF_0035:pg`, `PERF_0035:mysql`, `PERF_0035:spark`
  - remaining non-exact rows are now concentrated in `PERF_0006:mysql`, `PERF_0006:spark`, plus explicit `PORT` denominator rows
  - the retained post-93 frontier audit found `0` low-risk and `0` medium-risk recovery candidates under the unchanged route, denominator, and checker
  - `93 / 120` is therefore the current paper-safe ceiling for this Calcite HEP route
  - this is still evidence-ledger material, not timing, speedup, or leaderboard evidence
- This canary should not be merged into the canonical method-comparison row
  unless a separate denominator-aware policy is created.
- This non-PG expansion should also not be merged into the canonical
  method-comparison row unless a separate denominator-aware policy is created.
- The fail-closed `120`-row synthesis should not be merged into the canonical
  method-comparison row without a separate paper-readiness check and an
  explicit policy for mixed retained PG + bounded non-PG evidence rows.

## Do Not Claim

- Do not call
  [method_comparison_summary_v2.md](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.md)
  a leaderboard.
- Do not rank methods using subset-scoped rows as if denominators matched.
- Do not say R-Bot MySQL/Spark correctness is `0`.
- Do not say R-Bot full `120` timing exists.
- Do not say `speedup_transfer_rate` is computed.

## Paper-Safe Wording Snippets

Use this table-level framing:

`Table X is a denominator-aware evidence ledger, not a ranked leaderboard. Rows differ in route structure, engine scope, execution scope, and timing scope.`

Use this R-Bot PostgreSQL framing:

`For R-Bot, the current canonical paper-facing evidence is the PostgreSQL expansion v2 path, with generation on PG40 and timing only on the generated_pg15_from_pg40_expansion_match_exact_only subset.`

Use this R-Bot MySQL/Spark framing:

`Under the recovered R-Bot route, MySQL/Spark canary rows reached generation attempts, but produced no extractable final SQL. The retained responses contain rule-selection or rewrite-strategy text rather than executable target-engine SQL. Therefore, MySQL/Spark execution, timing, and speedup metrics remain not computed for R-Bot.`

Use this Calcite HEP MySQL/Spark framing:

`Calcite HEP was extended in a bounded MySQL/Spark canary with explicit target-dialect rendering. The canary generated 6/6 target-dialect SQL candidates and all 6 executed, but only 4/6 matched exactly. The two mismatches were both PERF_0006 and were caused by aggregate rewrite precision / decimal scale loss. Therefore this is useful boundary evidence, but not full MySQL/Spark correctness, timing, speedup, or leaderboard evidence.`

Use this Calcite HEP MySQL/Spark non-PG expansion framing:

`Calcite HEP was extended beyond PostgreSQL with explicit MySQL/Spark target-dialect rendering. In the bounded non-PG expansion, 80 MySQL/Spark rows were attempted for rewrite, 60 produced retained target-dialect SQL, and execution-validity on those 60 rows yielded 59 executed and 49 exact matches. This is bounded non-PG execution-validity evidence, not timing, speedup, leaderboard, or full 120-row comparable evidence.`

Use this Calcite HEP `120`-row fail-closed framing:

`Using retained PG40 route artifacts, the bounded non-PG MySQL/Spark expansion, and the bounded recovery canaries, Calcite HEP currently supports a fail-closed 120-row correctness ledger with 93 exact matches out of the intended 120-row tri-engine same-engine denominator. This ledger keeps parser, rewrite, setup, execution, and mismatch failures in-denominator as non-exact rows. It is useful paper evidence, but it is not timing, speedup, or leaderboard-comparable evidence.`

Use this Calcite HEP post-93 ceiling framing:

`Calcite HEP reaches a fail-closed exact-match ledger of 93/120 on the common_core_v0_40_same_engine_120 denominator. A post-93 frontier audit found no additional low-risk or medium-risk recovery candidates under the unchanged route, denominator, and checker. The remaining gaps are dominated by semantic mismatches, parser/deep-feature support gaps, or methodology-boundary PORT rows. Therefore 93/120 is the current paper-safe ceiling for this Calcite HEP route. This is bounded execution-validity evidence, not timing, speedup, leaderboard, or full 120-row comparable evidence.`

Use this SQLGlot route-level framing:

`SQLGlot transpile_same_dialect_noop is a same-engine 120-row route-level evidence row. It is denominator-aware route evidence, not cross-dialect portability evidence, not a full SQLGlot method-family aggregate, and not a leaderboard-comparable scalar. Unsupported, failed, and no-op rows remain explicit in denominator accounting.`

Use this SQLGlot optimize-route framing:

`SQLGlot optimize_same_dialect is a same-engine route-level evidence row. It is denominator-aware route evidence, not cross-dialect portability evidence, not a full SQLGlot method-family aggregate, and not a leaderboard-comparable scalar unless retained timing/speedup evidence explicitly supports that boundary.`

## Major Source Artifact Paths

- Canonical ledger:
  - [method_comparison_summary_v2.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2.csv)
- Ledger safety check:
  - [method_comparison_summary_v2_paper_readiness_check_v2.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/method_comparison_summary_v2_paper_readiness_check_v2.csv)
- R-Bot PG result card:
  - [r_bot_pg_expansion_result_card_v2.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_pg_expansion_result_card_v2.csv)
- R-Bot PG speedup summary:
  - [r_bot_pg15_speedup_summary_v2.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_pg15_speedup_summary_v2.csv)
- R-Bot MySQL/Spark canary boundary card:
  - [r_bot_mysql_spark_canary_result_card_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/r_bot_mysql_spark_canary_result_card_v1.csv)
- Calcite HEP MySQL/Spark canary boundary card:
  - [calcite_hep_mysql_spark_canary_result_card_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_mysql_spark_canary_result_card_v1.csv)
- Calcite HEP MySQL/Spark execution-expansion result card:
  - [calcite_hep_mysql_spark_execution_expansion_result_card_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_mysql_spark_execution_expansion_result_card_v1.csv)
- Calcite HEP fail-closed `120`-row synthesis:
  - [calcite_hep_120_fail_closed_synthesis_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_fail_closed_synthesis_v1.csv)
- Calcite HEP post-93 frontier audit:
  - [calcite_hep_120_post93_frontier_audit_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_post93_frontier_audit_v1.csv)
- Calcite HEP bounded recovery canary result card:
  - [calcite_hep_120_recovery_canary_08_result_card_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_recovery_canary_08_result_card_v1.csv)
- Calcite HEP bounded recovery round2 canary result card:
  - [calcite_hep_120_recovery_round2_canary_09_result_card_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_recovery_round2_canary_09_result_card_v1.csv)
- Calcite HEP bounded recovery round4b canary result card:
  - [calcite_hep_120_recovery_round4b_numeric_scale_canary_04_result_card_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_recovery_round4b_numeric_scale_canary_04_result_card_v1.csv)
- Calcite HEP bounded `PERF_0035` recovery canary result card:
  - [calcite_hep_120_recovery_perf0035_canary_03_result_card_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_120_recovery_perf0035_canary_03_result_card_v1.csv)
- Calcite HEP proposed method-comparison row:
  - [calcite_hep_method_comparison_proposed_row_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/calcite_hep_method_comparison_proposed_row_v1.csv)
- SQLGlot route audit:
  - [sqlglot_paper_route_audit_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_paper_route_audit_v1.csv)
- SQLGlot transpile_same_dialect_noop result card:
  - [sqlglot_transpile_same_dialect_noop_result_card_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_transpile_same_dialect_noop_result_card_v1.csv)
- SQLGlot proposed method-comparison row:
  - [sqlglot_method_comparison_proposed_row_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_method_comparison_proposed_row_v1.csv)
- SQLGlot optimize_same_dialect result card:
  - [sqlglot_optimize_same_dialect_result_card_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_optimize_same_dialect_result_card_v1.csv)
- SQLGlot optimize_same_dialect proposed row:
  - [sqlglot_optimize_same_dialect_proposed_row_v1.csv](/home/tianci_gao/code/sql-rewrite-bench/reports/evaluation/common_core_v0/sqlglot_optimize_same_dialect_proposed_row_v1.csv)
