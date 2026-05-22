# Section 8 Existing Values Patch v1

这个文件回答什么问题：给论文作者一个直接 patch guide，说明 Section 8 哪些值现在就能插，哪些只需要 aggregation，哪些必须人工复核，哪些需要新实验，哪些应该明确写成 NA / not computed。

注意：这里只给 patch guidance，不重写论文 prose，不改变 denominator、protocol、policy、claim boundary。

## 1. Values that can be inserted now

- `Table 8 / total cases` -> `40`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table1_common_core_composition_v1.csv
- `Table 8 / pool split` -> `PERF:16|CONS:9|PORT:9|LONGTAIL:6`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table1_common_core_composition_v1.csv
- `Table 8 / same-engine Track A rows` -> `120`
  source: reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv
- `Table 8 / source-family split` -> `Calcite:7|JOB/IMDB:2|PARROT:9|SQLStorm:3|Stack Queries:3|TPC-DS:7|TPC-H:7|VeriEQL:2`
  source: inventory/case_registry.csv|reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv
- `Table 9 / common-core tagged cases` -> `40/40 tagged; 0 missing`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `Table 9 / top tags overall` -> `plan_operator:present:scan:40|plan_operator:present:aggregate:34|plan_operator:present:join:32|plan_operator:present:sort:23|workload_realism:source_inherited:classic_analytical_baseline:16`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `Table 14 / planned/tested/blocked package hard negatives` -> `planned:120|tested:111|blocked:9`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_closure_summary_v1.csv
- `Table 14 / semantic rejections / false accepts` -> `semantic_rejections:111|false_accepts:0`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_rejection_mode_audit_v1.csv
- `Table 16 / Direct LLM exact timed slice` -> `timing_denom:94|gm:1.043634242319266|median:1.009402551073825|reg20_rate:0.03191489361702127`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Table 16 / SQLGlot optimize exact timed slice` -> `timing_denom:63|gm:0.9907164888740984|median:0.9951145947521497|reg20_rate:0.015873015873015872`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Table 17 / selected observability frontier identity` -> `selected PG plan-delta diagnostics retained plus separate failure-side exemplar`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_failure_exemplar_selection_v1.csv
- `Table 18 / PORT closure status` -> `bounded PORT6 only; full PORT9 not retained; SpeedupTransferRate NA_not_computed`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv
- `Table 19 / verifier support status` -> `SQLSolver smoke-only 3/4 support; VeriEQL canary 2-pair verdict split retained`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `Table 20 / conclusion-evidence map source` -> `paper_claim_matrix_v7 already retains claim/support/forbidden-overclaim layer`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv

## 2. Values that require aggregation but no new experiment

- `Table 9 / primary_vs_secondary_availability`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
  action: build axis-aware primary vs secondary summary from normalized tags
- `Table 9 / confirmed_vs_suspected_portability`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
  action: aggregate portability tag namespace by confirmed/suspected markers
- `Table 11 / r_bot / bounded prior evidence failure slicing readiness`
  source: reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
  action: use retained route failure summaries plus case tags where available
- `Table 11 / llm_r2 / bounded prior evidence failure slicing readiness`
  source: reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.csv|reports/evaluation/common_core_v0/llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.csv
  action: use retained route failure summaries plus case tags where available
- `Table 13 / SQLGlot combined executed`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
  action: build appendix-only aggregation from retained mixed-scope artifacts
- `Table 13 / SQLGlot combined exact`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
  action: build appendix-only aggregation from retained mixed-scope artifacts
- `Table 13 / SQLGlot combined timed`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
  action: build appendix-only aggregation from retained mixed-scope artifacts
- `Table 16 / sqlglot / sqlglot_combined_same_engine_240 median`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
  action: use retained timing summary or keep NA where the route is bounded-only
- `Table 16 / sqlglot / sqlglot_combined_same_engine_240 best_case`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
  action: use retained timing summary or keep NA where the route is bounded-only
- `Table 16 / sqlglot / sqlglot_combined_same_engine_240 worst_case`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
  action: use retained timing summary or keep NA where the route is bounded-only
- `Appendix B / full 4+1 taxonomy tag matrix`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_all_registry_cases_v1.csv
  action: use retained artifact directly or build a new appendix render where needed
- `Appendix C / taxonomy-aware failure slicing`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/case_level_failure_export_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
  action: use retained artifact directly or build a new appendix render where needed

## 3. Values that require manual review

- `Table 13 / LearnedRewrite generated`
  source: reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
  action: review mixed-scope or narrative-only appendix evidence before insertion
- `Table 13 / LearnedRewrite executed`
  source: reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
  action: review mixed-scope or narrative-only appendix evidence before insertion
- `Appendix I / reproducibility package`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/common_core_v0_paper_results_readme_v10.md|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_results_table_index_v5.csv
  action: use retained artifact directly or build a new appendix render where needed

## 4. Values that require additional experiment

- `Table 18 / full PORT9 closure`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv
  action: requires explicit PORT9 closure packet
- `Table 18 / full PORT registry closure`
  source: inventory/case_registry.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv
  action: requires a broader registry-level portability packet
- `Table 18 / target-engine paired timing evidence`
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv
  action: needs retained paired target-engine exact timed transfer packet

## 5. Values that must remain NA / not computed

- `Table 13 / SQLGlot combined GM` -> `not_supported_write_NA`
  boundary: all method rows remain leaderboard_comparable=no unless explicit policy says otherwise
- `Table 13 / SQLGlot combined Regression@20` -> `not_supported_write_NA`
  boundary: all method rows remain leaderboard_comparable=no unless explicit policy says otherwise
- `Table 13 / LLM-R2 original timed` -> `not_supported_write_NA`
  boundary: all method rows remain leaderboard_comparable=no unless explicit policy says otherwise
- `Table 13 / LLM-R2 original GM` -> `not_supported_write_NA`
  boundary: all method rows remain leaderboard_comparable=no unless explicit policy says otherwise
- `Table 13 / LLM-R2 original Regression@20` -> `not_supported_write_NA`
  boundary: all method rows remain leaderboard_comparable=no unless explicit policy says otherwise
- `Table 13 / LLM-R2 recovered timed` -> `not_supported_write_NA`
  boundary: all method rows remain leaderboard_comparable=no unless explicit policy says otherwise
- `Table 13 / LLM-R2 recovered GM` -> `not_supported_write_NA`
  boundary: all method rows remain leaderboard_comparable=no unless explicit policy says otherwise
- `Table 13 / LLM-R2 recovered Regression@20` -> `not_supported_write_NA`
  boundary: all method rows remain leaderboard_comparable=no unless explicit policy says otherwise
- `Table 13 / LearnedRewrite timed` -> `not_supported_write_NA`
  boundary: all method rows remain leaderboard_comparable=no unless explicit policy says otherwise
- `Table 13 / LearnedRewrite GM` -> `not_supported_write_NA`
  boundary: all method rows remain leaderboard_comparable=no unless explicit policy says otherwise
- `Table 13 / LearnedRewrite Regression@20` -> `not_supported_write_NA`
  boundary: all method rows remain leaderboard_comparable=no unless explicit policy says otherwise
- `Table 16 / sqlglot / sqlglot_combined_same_engine_240 win` -> `NA_not_found`
  boundary: speedup valid only on exact plus timing-success rows
- `Table 16 / sqlglot / sqlglot_combined_same_engine_240 tie` -> `NA_not_found`
  boundary: speedup valid only on exact plus timing-success rows
- `Table 16 / sqlglot / sqlglot_combined_same_engine_240 loss` -> `NA_not_found`
  boundary: speedup valid only on exact plus timing-success rows
- `Table 18 / SpeedupTransferRate` -> `NA_not_computed`
  boundary: requires paired target-engine timing arrays or repeated runtime summaries
- `Table 19 / SQLSolver prove` -> `NA_not_found`
  boundary: do not place verifier support into same-engine speedup evidence
- `Table 19 / SQLSolver refute` -> `NA_not_found`
  boundary: do not place verifier support into same-engine speedup evidence
- `Table 19 / SQLSolver unknown` -> `NA_not_found`
  boundary: do not place verifier support into same-engine speedup evidence
- `Table 19 / SQLSolver timeout` -> `NA_not_found`
  boundary: do not place verifier support into same-engine speedup evidence

## 6. Claim boundaries to preserve

- Common-core v0 denominator is fixed at 40 cases with a Track A same-engine expansion to 120 rows.
- Track A same-engine rewrite, Track B observability/support, and Track C portability/translation must remain separate.
- The paper table is a denominator-aware evidence ledger, not a ranked leaderboard.
- All method rows remain leaderboard_comparable = no unless an existing admission policy explicitly says otherwise.
- Speedup is valid only on exact + timing-success rows.
- SpeedupTransferRate remains NA unless paired target-engine timing evidence exists.
- Bounded PORT6 closure must not be rewritten as full PORT9 or full PORT registry closure.
- SQLSolver and VeriEQL remain verifier support evidence, not rewrite-generation baselines.
