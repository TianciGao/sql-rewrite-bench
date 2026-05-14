# Table Regeneration Commands v1

This file lists exact retained commands or runner entrypoints when they are explicitly present in the artifact tree. If no exact command is frozen, the row is marked as not retained rather than reconstructed from memory.

## Denominator composition

No dedicated regeneration command retained. Canonical retained artifacts are `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table1_common_core_composition_v1.csv` and `reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv`.

## Taxonomy coverage

No dedicated regeneration command retained for the Round 2 aggregation packet. Canonical outputs are under `reports/evaluation/common_core_v0/09_TAXONOMY_COVERAGE_V1/`.

## Hard-negative guardrail

Retained packet runner exists: `python -B reports/evaluation/common_core_v0/runs/package_hard_negative_closure_01/run_package_hard_negative_closure.py` and `bash reports/evaluation/common_core_v0/runs/package_hard_negative_closure_01/run_manual_package_hard_negative_closure.sh`.

## Candidate failure accounting

No dedicated regeneration command retained for the Round 3 aggregation table; canonical outputs are under `reports/evaluation/common_core_v0/10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1/`.

## Speedup slices

Canonical route-level source is `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv`. Upstream retained timing runners include `bash reports/evaluation/common_core_v0/runs/direct_llm_same_engine_timing_01/run_manual_direct_llm_timing.sh`, `bash reports/evaluation/common_core_v0/runs/sqlglot_full_per_case_timing_01/run_manual_sqlglot_full_per_case_timing.sh`, `bash reports/evaluation/common_core_v0/runs/calcite_hep_93_exact_timing_01/run_manual_calcite_hep_93_exact_timing.sh`, and `bash reports/evaluation/common_core_v0/runs/r_bot_pg15_timing_expansion_02/run_manual_r_bot_pg15_timing.sh`.

## Selected observability frontier

Canonical frontier sources are `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv` and `reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/selected_plan_observability_frontier_v1.csv`. Upstream retained PG runner exists: `python -B reports/evaluation/common_core_v0/runs/pg_plan_attribution_113_01/run_pg_plan_attribution_113.py` and `bash reports/evaluation/common_core_v0/runs/pg_plan_attribution_113_01/run_manual_pg_plan_attribution_113.sh`.

## PORT readiness

No dedicated regeneration command retained for the Round 5 PORT readiness tables. Canonical outputs are under `reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1/`.

## Verifier support

No dedicated regeneration command retained for the Round 5 verifier support ledger. Canonical outputs are under `reports/evaluation/common_core_v0/12_PORT_VERIFIER_ARTIFACT_MAP_V1/`.

## Final Section 8 tables

No retained final render command was found, and `reports/evaluation/common_core_v0/13_SECTION8_FINAL_RENDER_V1/` is absent in the inspected tree. Submission packaging should therefore cite the Round 1-5 artifact map rather than an already-frozen final render command.
