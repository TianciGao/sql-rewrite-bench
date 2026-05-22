# Table 12 Method Evidence Ledger Regenerated V1

## Purpose
Static regeneration of Section 8 Table 12 from retained Common-core v0 artifacts.

## Regenerated Table 12
|method / route|Scope|Planned|Generated / Ready|Executed|Exact|Timed|GM|Regression@20|Placement|
|---|---|---|---|---|---|---|---|---|---|
|Direct LLM original|tri-engine same-engine|120|120 generated; 115 ready|99|94|94|1.043634242319266|0.03191489361702127|main same-engine evidence|
|Direct LLM + Repair-1|tri-engine feedback route|120|120 generated; 5 preflight-blocked|97|96|96|1.0430582867389244|0.041666666666666664|route-level evidence; mixed-source timing|
|SQLGlot optimize|tri-engine route|120|120 attempted; 75 generated|65|63|63|0.9907164888740984|0.015873015873015872|revised exact63 route|
|SQLGlot no-op|tri-engine route|120|120 attempted; 78 generated|72|72|72|1.000145903000493|0.013888888888888888|no-op / low-transform route|
|Calcite HEP fail-closed|tri-engine fail-closed route|120|retained route artifacts|95|93|93|0.995917121478|0.0752688172043|correctness-gated timing packet|
|R-Bot|mixed scope|formal 120 generation|PG-scoped subsets|15 PG-only|15 PG-only|15|0.9218248321470981|0.2|bounded / mixed appendix|
|LLM-R2 original|PG-only bounded|9|9|3 exact + 6 execution failed|3|0|NA|NA|bounded appendix|
|LLM-R2 recovered|PG9 recovery audit|9|9|6|6|0|NA|NA|PG6 exact recovered subset|
|LearnedRewrite|PG10 bounded|10|10|NA_not_retained|10 checker-consistent|NA|NA|NA|bounded appendix; 8 source-like/no-op|

## Source Artifacts
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/calcite_hep_93_exact_timing_result_card_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/sqlglot_full_per_case_timing_result_card_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/sqlglot_result_check_backfill_summary_v1.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v2.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv`
- `reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv`
- `reports/evaluation/common_core_v0/10_HARD_NEGATIVE_FAILURE_ACCOUNTING_V1/candidate_failure_accounting_v1.csv`
- `reports/evaluation/common_core_v0/calcite_hep_120_fail_closed_synthesis_v1.csv`
- `reports/evaluation/common_core_v0/direct_llm_same_engine_result_card_v1.csv`
- `reports/evaluation/common_core_v0/llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.csv`
- `reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md`
- `reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.csv`
- `reports/evaluation/common_core_v0/runs/sqlglot_full_per_case_timing_01/timing_summary.csv`

## Semantic Checks
- Direct LLM + Repair-1 executed = exact + mismatch = 97 / 96 + 1; ready_after_preflight 115 is not executed.
- SQLGlot optimize uses exact63/timed63 and canonical GM 0.9907164888740984.
- SQLGlot no-op preserves exact72/timed72 and source-like/no-op boundary.
- Calcite HEP uses exact93/timed93 and canonical GM 0.995917121478.
- R-Bot remains mixed-scope / PG15 bounded appendix evidence.
- LLM-R2 recovered preserves PG9 recovery audit / PG6 exact recovered subset boundary.
- LearnedRewrite remains bounded PG10 with 8 source-like/no-op rows and no inferred execution/timing.
- All Round 4 canonical GM speedup values are retained.
- No obsolete draft GM values appear in regenerated metric cells.

## Boundaries
- Direct LLM repair executed is `97`, computed as `96 exact + 1 mismatch`; ready/preflight values are not executed.
- SQLGlot optimize uses the revised exact63 timing row, not older exact65 or old draft GM values.
- R-Bot, LLM-R2, and LearnedRewrite remain bounded appendix evidence.
- Speedup metrics apply only on exact + timing-success rows.

## Not A Ranked Leaderboard
This regenerated table is not a ranked leaderboard and does not name a winner.
