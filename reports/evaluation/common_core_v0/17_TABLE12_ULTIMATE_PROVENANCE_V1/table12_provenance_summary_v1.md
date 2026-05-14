# Table 12 Ultimate Provenance Audit V1

## 1. Purpose
This audit recursively traces Section 8 Table 12, the Common-core v0 denominator-aware method evidence ledger, from each paper-facing cell to retained source artifacts, upstream artifacts, retained runners where present, and formula or extraction logic.

## 2. Scope and non-goals
The audit is read-only. It did not run database engines, LLM/model calls, verifier experiments, PORT9 experiments, EXPLAIN collection, timing collection, or table regeneration. It did not change registries, taxonomy, case facts, protocol, code, or paper prose. The final render directory was absent, so the task-provided draft Table 12 values were treated as the target value set.

## 3. Table 12 Value Lineage Overview
The audit wrote 90 cell-level provenance rows covering nine method/route rows and ten Table 12 columns. Trace statuses are: {'traceable_to_artifact_chain': 40, 'fully_traceable_to_runner_and_artifact': 31, 'traceable_to_static_policy': 18, 'artifact_only_no_generator_retained': 1}. Generator statuses are: {'local_aggregation_script_not_retained': 19, 'upstream_runner_retained': 34, 'static_policy_no_generator_needed': 9, 'artifact_only_generator_missing': 19, 'not_applicable': 9}. Recompute statuses are: {'not_recomputed': 27, 'recomputed_exact': 28, 'recomputed_rounded': 4, 'artifact_only_accepted': 21, 'expected_NA': 10}.

## 4. Immediate Source Tables
The primary immediate sources are `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv` for main route method evidence, `reports/evaluation/common_core_v0/10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1/candidate_failure_accounting_v1.csv` for executed/failure semantics and bounded appendix rows, and `reports/evaluation/common_core_v0/11_TIMING_OBSERVABILITY_V1/speedup_slice_summary_v1.csv` / `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv` for timing cells. Bounded method placement also uses `table11_bounded_pilot_evidence_reuse_v3.csv` and route-specific reconciliation artifacts.

## 5. Recursive Source Tracing Results
Table 3 traces onward to route result cards, timing tables, and source event artifacts, but no dedicated Table 3 regeneration script was found. Candidate failure accounting traces to `table7_failure_accounting_matrix_v3.csv`, `method_candidate_rejection_accounting_v1.csv`, `case_level_failure_export_v1.csv`, and route result/reconciliation artifacts, but no dedicated regeneration script was found. Speedup slice summary traces to Table 6 and timing packets; main route timing cells further trace to timing event rows and retained timing runners.

## 6. Generator Scripts Found
Retained upstream runners were found for Direct LLM generation/execution/timing, Direct LLM repair, SQLGlot timing, Calcite HEP execution/timing, and R-Bot PG-scoped generation/execution/timing. The Direct LLM repair runner and Calcite/SQLGlot timing scripts retain GM speedup and Regression@20 formula code. Fully runner-traceable Table 12 cells are the main-route generated/executed/exact/timed/speedup cells where the value can be followed to a retained runner and retained event or summary artifact.

## 7. Generator Scripts Not Retained
`table3_same_engine_method_evidence_v3.csv` does not have a retained dedicated generator script. `candidate_failure_accounting_v1.csv` does not have a retained dedicated generator script. `speedup_slice_summary_v1.csv` does not have a retained dedicated generator script; only upstream timing runners and Table 6/speedup artifacts are retained. Several bounded appendix reconciliations, especially LearnedRewrite and LLM-R2 summary/review artifacts, are artifact-chain only.

## 8. Formula And Identity Checks
Executed semantics are preserved: executed means successful execution returning a result, not ready_after_preflight. Direct LLM + Repair-1 executed=97 provenance is from candidate failure accounting with `executed = exact + mismatch = 97` / `96 + 1`; the retained 115 ready/preflight value is not treated as executed. GM speedup uses `exp(mean(log(speedup_ratio)))`, with `speedup_ratio = source_median_runtime / rewrite_median_runtime` where retained. Regression@20 uses `count(speedup_ratio < 0.8) / timing_denominator`.

## 9. Route-Specific Provenance Notes
Direct LLM original traces to its result card, run event artifacts, and exact-timed timing packet. Direct LLM repair traces to the retained repair runner, result card, repair result summary, and mixed-source final timing summary. SQLGlot optimize uses the revised exact63 route; older exact65 route-card wording is not the canonical Table 12 value. SQLGlot no-op preserves the no-op/source-like route boundary. Calcite HEP uses the 93 exact-row correctness-gated timing packet. R-Bot remains mixed-scope appendix evidence. LLM-R2 recovered is a PG9 audit with PG6 exact recovered subset provenance, not a standalone PG6 denominator row. LearnedRewrite remains bounded PG10 evidence with 8 source-like/no-op rows and no inferred executed/timing cells.

## 10. Risks And Caveats
The main hardening risk is generator absence for the local aggregation layers. Table 3, candidate failure accounting, and speedup slice summary are retained and auditable, but their exact regeneration scripts are missing. There are also known artifact-version caveats: Direct LLM repair Table 3 executed wording is unsafe if read as final executed semantics, and the older SQLGlot optimize result card reports exact65 while the retained paper-safe row is exact63 after checker backfill.

## 11. Recommended Hardening Actions
Write formal static regeneration scripts for Table 3, candidate failure accounting, and speedup slice summary from retained artifacts without changing values. Add a small consistency check that fails if Direct LLM repair executed is computed from ready_after_preflight instead of exact+mismatch. Add an explicit obsolete/superseded marker to older SQLGlot optimize exact65 route-card fields.

## 12. Source-of-Truth Writeback Judgment
No source-of-truth writeback is required from this audit. The recommended action is hardening provenance generators, not changing metrics, denominators, registry facts, taxonomy, case facts, protocol, or paper claims.
