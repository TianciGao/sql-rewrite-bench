# Paper Artifact Index v1

## Purpose

这个文件回答什么问题：把 Section 8 和 Appendix A-I 的 retained artifacts 映射成一个 paper-facing index，而不生成任何新 claim。

## Main Section 8 artifact map

| paper_location | table_or_appendix | artifact_path | status | claim_boundary |
| --- | --- | --- | --- | --- |
| Section 8.2 | Table 8 denominator composition | reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_existing_values_patch_v1.csv | ready | fixed denominator only |
| Section 8.3 | Table 9 taxonomy coverage | reports/evaluation/common_core_v0/09_TAXONOMY_COVERAGE_V1/common_core_v0_taxonomy_coverage_v1.csv | ready | benchmark characterization only not method ranking |
| Section 8.3 | Table 10 pool taxonomy coverage | reports/evaluation/common_core_v0/09_TAXONOMY_COVERAGE_V1/common_core_v0_taxonomy_by_pool_v1.csv | ready | pool stress characterization only |
| Section 8.3 | Table 11 taxonomy-aware failure slicing readiness | reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_missing_data_ledger_v1.csv | aggregation_ready | readiness only not final rendered failure slicing table |
| Section 8.5 | Table 13 method evidence ledger | reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_missing_data_ledger_v1.csv | aggregation_ready | do not promote bounded prior methods into main same-engine rows |
| Section 8.6 | Table 14 hard-negative guardrail | reports/evaluation/common_core_v0/10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1/hard_negative_guardrail_ledger_v1.csv | ready | package hard-negative controls only not method candidate failures |
| Section 8.6 | Table 15 candidate failure accounting | reports/evaluation/common_core_v0/10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1/candidate_failure_accounting_v1.csv | ready_with_boundary | candidate failures only not package hard-negative rejection and bounded routes stay bounded |
| Section 8.7 | Table 16 speedup slices | reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/speedup_slice_summary_v1.csv | ready_with_boundary | exact plus timing-success rows only; not a ranked leaderboard |
| Section 8.7 | Table 17 selected observability frontier | reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/selected_plan_observability_frontier_v1.csv | ready_with_boundary | selected PG frontier only not full NodeAlignmentCoverage or denominator-wide causal attribution |
| Section 8.8 | Table 18 PORT closure / readiness | reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1/port_bounded_route_closure_v1.csv | ready_with_boundary | not_full_PORT9; not_full_PORT_registry; not transfer-speed evidence |
| Section 8.9 | Table 19 verifier support | reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1/verifier_support_pair_ledger_v1.csv | ready_with_boundary | verifier support only not rewrite generation and not same-engine 120 denominator |
| Section 8.10 | Table 20 conclusion-evidence map | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv | ready | map claims to retained evidence only and do not create new claims |
| Section 8.8 | Table 18 SpeedupTransferRate field | reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1/speedup_transfer_readiness_v1.csv | not_supported_write_NA | missing paired target-engine timing arrays or repeated runtime summaries |
| Section 8.7 | Table 17 full NodeAlignmentCoverage | reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_remaining_experiment_gaps_v8.csv | new_experiment_needed | do not claim denominator-wide NodeAlignmentCoverage |

## Appendix artifact map

| paper_location | table_or_appendix | artifact_path | status | claim_boundary |
| --- | --- | --- | --- | --- |
| Appendix A | Common-core case list | reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv | ready | case list only |
| Appendix B | Full 4+1 taxonomy tag matrix | reports/evaluation/common_core_v0/09_TAXONOMY_COVERAGE_V1/common_core_v0_case_tag_matrix_v1.csv | ready | retained tags only; no inferred tags |
| Appendix C | Taxonomy-aware failure slicing | reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_missing_data_ledger_v1.csv | aggregation_ready | requires aggregation from retained failure exports; no new experiment needed |
| Appendix D | Hard-negative per-case/per-engine ledger | reports/evaluation/common_core_v0/10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1/hard_negative_guardrail_ledger_v1.csv | ready | package controls only |
| Appendix E | Route-level method cards | reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_missing_data_ledger_v1.csv | aggregation_ready | main-track and bounded rows remain separate |
| Appendix F | Selected plan observability frontier | reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/selected_plan_observability_frontier_v1.csv | ready_with_boundary | selected frontier only not denominator-wide attribution |
| Appendix G | PORT bounded closure and SpeedupTransferRate readiness | reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1/speedup_transfer_readiness_v1.csv | ready_with_boundary | SpeedupTransferRate not computed; missing paired target-engine timing |
| Appendix H | Verifier support details | reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1/verifier_support_pair_ledger_v1.csv | ready_with_boundary | support-only evidence not rewrite baselines |
| Appendix I | Reproducibility package | reports/evaluation/common_core_v0/08_SECTION8_EVIDENCE_FREEZE_V1/section8_missing_data_ledger_v1.csv | manual_review_needed | scope and packaging boundary still need human review |

## Artifacts ready now

- ready = 8
- ready_with_boundary = 8

## Aggregation-ready artifacts

- aggregation_ready = 4

## Manual review needed

- manual_review_needed = 1

## New experiment needed

- new_experiment_needed = 1

## Explicit NA / not computed fields

- not_supported_write_NA = 1
- Explicit NA remains necessary for `SpeedupTransferRate`.
- Denominator-wide NodeAlignmentCoverage remains a future experiment rather than a currently ready table field.

## Safe prose for reproducibility appendix

The artifact index maps each Section 8 or Appendix location to retained evidence, its denominator, and its claim boundary. It should be used to assemble a denominator-aware paper package, not to invent new metrics or broaden retained evidence beyond its frozen scope.
