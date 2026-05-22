# Section 8 Missing Data Ledger v1

这个文件回答什么问题：逐表说明 Section 8 里哪些值已经被现有 freeze artifact 直接支持，哪些还能从现有 artifact 计算，哪些需要新的聚合、人工复核、新实验，或者必须保持 NA / not computed。

关键边界：这是 evidence ledger，不是排行榜；不运行 DB / model / verifier；Track A same-engine、Track B observability/support、Track C portability/translation 必须分开。

## 8.2 Table 8

### What can be filled now

- `total_cases` -> `40`
  action: insert directly from retained denominator composition table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table1_common_core_composition_v1.csv
  notes: Accepted denominator contract.
- `pool_count_performance` -> `16`
  action: insert directly from retained pool split
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table1_common_core_composition_v1.csv
- `pool_count_consistency` -> `9`
  action: insert directly from retained pool split
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table1_common_core_composition_v1.csv
- `pool_count_portability` -> `9`
  action: insert directly from retained pool split
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table1_common_core_composition_v1.csv
- `pool_count_longtail` -> `6`
  action: insert directly from retained pool split
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table1_common_core_composition_v1.csv
- `same_engine_row_count` -> `120`
  action: insert direct denominator row count
  source: reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv
- `denominator_id` -> `common_core_v0_40_same_engine_120`
  action: insert explicit denominator id
  source: reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv

### What is computable from existing artifacts

- `source_family_split` -> `Calcite:7|JOB/IMDB:2|PARROT:9|SQLStorm:3|Stack Queries:3|TPC-DS:7|TPC-H:7|VeriEQL:2`
  action: aggregate common-core case_ids against case_registry source_family
  source: inventory/case_registry.csv|reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv
  notes: Computed from registry plus frozen common-core manifest.

### Claim boundary

- 40 cases x 3 engines only
- do not infer source families from prose
- do not restate as approximate split
- keep Track A denominator separate from Track B and Track C
- use frozen common-core v0 denominator only

## 8.3 Table 9

### What is computable from existing artifacts

- `distinct_tags_sql_feature` -> `11`
  action: count distinct normalized tags by axis over common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `cases_covered_sql_feature` -> `32`
  action: count common-core cases with at least one tag in the axis
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `distinct_tags_rewrite_opportunity` -> `18`
  action: count distinct normalized tags by axis over common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `cases_covered_rewrite_opportunity` -> `40`
  action: count common-core cases with at least one tag in the axis
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `distinct_tags_plan_operator` -> `11`
  action: count distinct normalized tags by axis over common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `cases_covered_plan_operator` -> `40`
  action: count common-core cases with at least one tag in the axis
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `distinct_tags_workload_realism` -> `8`
  action: count distinct normalized tags by axis over common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `cases_covered_workload_realism` -> `32`
  action: count common-core cases with at least one tag in the axis
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `distinct_tags_portability` -> `9`
  action: count distinct normalized tags by axis over common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `cases_covered_portability` -> `24`
  action: count common-core cases with at least one tag in the axis
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_tags_overall` -> `plan_operator:present:scan:40|plan_operator:present:aggregate:34|plan_operator:present:join:32|plan_operator:present:sort:23|workload_realism:source_inherited:classic_analytical_baseline:16`
  action: aggregate normalized tag frequency over common-core 40
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv

### What requires aggregation

- `primary_vs_secondary_availability` -> `primary_tags:17|secondary_tags:12`
  action: build axis-aware primary vs secondary summary from normalized tags
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `confirmed_vs_suspected_portability` -> `confirmed:6|suspected:3`
  action: aggregate portability tag namespace by confirmed/suspected markers
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv

### Claim boundary

- case-level tags only
- do not infer from taxonomy prose alone
- keep confirmed and suspected portability separate
- report as retained tag frequency, not semantic importance ranking
- requires a new aggregation table, not a new experiment

## 8.3 Table 10

### What is computable from existing artifacts

- `top_sql_feature_performance` -> `sql_feature:primary:date_time_function:6|sql_feature:primary:correlated_subquery:3|sql_feature:primary:cte:3|sql_feature:secondary:expression_complexity:2|sql_feature:secondary:subquery_in_from:2`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_sql_feature_consistency` -> `sql_feature:primary:correlated_subquery:7|sql_feature:primary:outer_join:3|sql_feature:primary:subquery_in_from:1|sql_feature:primary:set_operation:1|sql_feature:secondary:subquery_in_from:1`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_sql_feature_portability` -> `sql_feature:primary:date_time_function:5|sql_feature:primary:expression_complexity:4|sql_feature:secondary:expression_complexity:1`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_sql_feature_longtail` -> `sql_feature:primary:cte:5|sql_feature:primary:window_function:3|sql_feature:secondary:expression_complexity:3|sql_feature:secondary:outer_join:2|sql_feature:primary:outer_join:2`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_rewrite_opportunity_performance` -> `rewrite_opportunity:primary:predicate_pushdown:7|rewrite_opportunity:secondary:predicate_pushdown:7|rewrite_opportunity:secondary:join_reorder:4|rewrite_opportunity:secondary:materialization_strategy:3|rewrite_opportunity:primary:subquery_decorrelation:3`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_rewrite_opportunity_consistency` -> `rewrite_opportunity:primary:subquery_decorrelation:6|rewrite_opportunity:secondary:aggregation_rewrite:2|rewrite_opportunity:primary:aggregation_rewrite:2|rewrite_opportunity:secondary:materialization_strategy:1|rewrite_opportunity:primary:order_limit_simplification:1`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_rewrite_opportunity_portability` -> `rewrite_opportunity:primary:dialect_adaptation:9|rewrite_opportunity:secondary:function_normalization:5|rewrite_opportunity:secondary:expression_simplification:4|rewrite_opportunity:secondary:order_limit_simplification:3`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_rewrite_opportunity_longtail` -> `rewrite_opportunity:secondary:aggregation_rewrite:5|rewrite_opportunity:primary:cte_strategy:4|rewrite_opportunity:primary:expression_simplification:1|rewrite_opportunity:secondary:cte_strategy:1|rewrite_opportunity:primary:materialization_strategy:1`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_plan_operator_performance` -> `plan_operator:present:aggregate:16|plan_operator:present:scan:16|plan_operator:present:join:14|plan_operator:present:sort:12|plan_operator:present:limit:8`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_plan_operator_consistency` -> `plan_operator:present:scan:9|plan_operator:present:join:8|plan_operator:present:subquery:7|plan_operator:present:aggregate:7|plan_operator:present:sort:2`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_plan_operator_portability` -> `plan_operator:present:scan:9|plan_operator:present:filter:7|plan_operator:present:aggregate:5|plan_operator:present:join:4|plan_operator:present:limit:3`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_plan_operator_longtail` -> `plan_operator:present:aggregate:6|plan_operator:present:join:6|plan_operator:present:scan:6|plan_operator:present:sort:6|plan_operator:present:subquery:6`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_workload_realism_performance` -> `workload_realism:source_inherited:classic_analytical_baseline:16|workload_realism:source_inherited:real_data_correlation:2|workload_realism:case_specific:long_tail_structure:1|workload_realism:case_specific:complex_expression_density:1`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_workload_realism_consistency` -> `workload_realism:case_specific:long_tail_structure:1`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_workload_realism_portability` -> `workload_realism:source_inherited:realistic_query_style:9|workload_realism:case_specific:complex_expression_density:4|workload_realism:case_specific:result_size_sensitivity:3`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_workload_realism_longtail` -> `workload_realism:source_inherited:realistic_query_style:6|workload_realism:case_specific:long_tail_structure:4|workload_realism:source_inherited:manual_gap_fill_realism:3|workload_realism:case_specific:complex_expression_density:2|workload_realism:case_specific:result_size_sensitivity:1`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_portability_risk_performance` -> `portability:suspected:datetime_semantics_gap:6|portability:suspected:type_semantics_gap:3|portability:confirmed:limit_fetch_gap:2`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_portability_risk_consistency` -> `portability:confirmed:null_semantics_gap:2|portability:suspected:null_semantics_gap:1|portability:confirmed:limit_fetch_gap:1`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_portability_risk_portability` -> `portability:confirmed:identifier_quoting:9|portability:confirmed:type_semantics_gap:6|portability:confirmed:datetime_semantics_gap:5|portability:confirmed:limit_fetch_gap:3|portability:confirmed:boolean_semantics_gap:2`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
- `top_portability_risk_longtail` -> `portability:suspected:null_semantics_gap:1|portability:suspected:datetime_semantics_gap:1`
  action: aggregate top normalized tags by pool and axis from common-core tag matrix
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv

### Claim boundary

- pool-level retained tag coverage only

## 8.3 Table 11

### What can be filled now

- `direct_llm / direct_llm_same_engine_rewrite failure slicing readiness` -> `filled_from_existing_artifact`
  action: use retained route failure summaries plus case tags where available
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/case_level_failure_export_v1.csv
  notes: route summary plus 120-row case-level export are retained
- `calcite_hep / calcite_hep_fail_closed_120 failure slicing readiness` -> `filled_from_existing_artifact`
  action: use retained route failure summaries plus case tags where available
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/case_level_failure_export_v1.csv
  notes: route summary and case-level failures retained

### What is computable from existing artifacts

- `sqlglot / sqlglot_optimize_same_dialect failure slicing readiness` -> `computable_from_existing_artifact`
  action: use retained route failure summaries plus case tags where available
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/case_level_failure_export_v1.csv
  notes: route summary retained and case-level export can be filtered by route
- `sqlglot / sqlglot_transpile_same_dialect_noop failure slicing readiness` -> `computable_from_existing_artifact`
  action: use retained route failure summaries plus case tags where available
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/case_level_failure_export_v1.csv
  notes: route summary retained and case-level export can be filtered by route

### What requires aggregation

- `r_bot / bounded prior evidence failure slicing readiness` -> `requires_new_aggregation`
  action: use retained route failure summaries plus case tags where available
  source: reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
  notes: mixed-scope appendix evidence needs a dedicated taxonomy-aware slicing summary
- `llm_r2 / bounded prior evidence failure slicing readiness` -> `requires_new_aggregation`
  action: use retained route failure summaries plus case tags where available
  source: reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.csv|reports/evaluation/common_core_v0/llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.csv
  notes: bounded PG evidence exists but needs explicit taxonomy-aware slicing summary

### Claim boundary

- do not infer tags from source family names

## 8.5 Table 13

### What can be filled now

- `Direct LLM planned` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Direct LLM generated` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Direct LLM executed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Direct LLM exact` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Direct LLM timed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Direct LLM GM` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Direct LLM Regression@20` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot optimize planned` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot optimize generated` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot optimize executed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot optimize exact` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot optimize timed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot optimize GM` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot optimize Regression@20` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot no-op planned` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot no-op generated` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot no-op executed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot no-op exact` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot no-op timed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot no-op GM` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot no-op Regression@20` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot combined planned` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot combined generated` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Calcite HEP fail-closed planned` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Calcite HEP fail-closed generated` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Calcite HEP fail-closed executed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Calcite HEP fail-closed exact` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Calcite HEP fail-closed timed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Calcite HEP fail-closed GM` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Calcite HEP fail-closed Regression@20` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table3_same_engine_method_evidence_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `Calcite HEP PG timing planned` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
- `Calcite HEP PG timing generated` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
- `Calcite HEP PG timing executed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
- `Calcite HEP PG timing exact` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
- `Calcite HEP PG timing timed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
- `Calcite HEP PG timing GM` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
- `Calcite HEP PG timing Regression@20` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
- `R-Bot planned` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/r_bot_formal_result_card_v1.csv|reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.csv
- `R-Bot generated` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/r_bot_formal_result_card_v1.csv|reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.csv
- `R-Bot executed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/r_bot_formal_result_card_v1.csv|reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.csv
- `R-Bot exact` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/r_bot_formal_result_card_v1.csv|reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.csv
- `R-Bot timed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/r_bot_formal_result_card_v1.csv|reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.csv
- `R-Bot GM` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/r_bot_formal_result_card_v1.csv|reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.csv
- `R-Bot Regression@20` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/r_bot_formal_result_card_v1.csv|reports/evaluation/common_core_v0/r_bot_common_core_120_evidence_reconciliation_v1.csv
- `LLM-R2 original planned` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.csv
- `LLM-R2 original generated` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.csv
- `LLM-R2 original executed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.csv
- `LLM-R2 original exact` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.csv
- `LLM-R2 recovered planned` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.csv
- `LLM-R2 recovered generated` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.csv
- `LLM-R2 recovered executed` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.csv
- `LLM-R2 recovered exact` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.csv
- `LearnedRewrite planned` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
- `LearnedRewrite exact` -> `filled_from_existing_artifact`
  action: insert route-level value directly from retained artifact
  source: reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv

### What requires aggregation

- `SQLGlot combined executed` -> `requires_new_aggregation`
  action: build appendix-only aggregation from retained mixed-scope artifacts
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot combined exact` -> `requires_new_aggregation`
  action: build appendix-only aggregation from retained mixed-scope artifacts
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot combined timed` -> `requires_new_aggregation`
  action: build appendix-only aggregation from retained mixed-scope artifacts
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv

### What requires manual review

- `LearnedRewrite generated` -> `requires_manual_review`
  action: review mixed-scope or narrative-only appendix evidence before insertion
  source: reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
- `LearnedRewrite executed` -> `requires_manual_review`
  action: review mixed-scope or narrative-only appendix evidence before insertion
  source: reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv

### What must stay NA / not computed

- `SQLGlot combined GM` -> `not_supported_write_NA`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `SQLGlot combined Regression@20` -> `not_supported_write_NA`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `LLM-R2 original timed` -> `not_supported_write_NA`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.csv
- `LLM-R2 original GM` -> `not_supported_write_NA`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.csv
- `LLM-R2 original Regression@20` -> `not_supported_write_NA`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/llm_r2_pg9_bounded_evidence_reconciliation_v1.csv
- `LLM-R2 recovered timed` -> `not_supported_write_NA`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.csv
- `LLM-R2 recovered GM` -> `not_supported_write_NA`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.csv
- `LLM-R2 recovered Regression@20` -> `not_supported_write_NA`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.csv
- `LearnedRewrite timed` -> `not_supported_write_NA`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
- `LearnedRewrite GM` -> `not_supported_write_NA`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv
- `LearnedRewrite Regression@20` -> `not_supported_write_NA`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/prior_methods_pg10_bounded_appendix_v1.md|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table11_bounded_pilot_evidence_reuse_v3.csv

### Claim boundary

- all method rows remain leaderboard_comparable=no unless explicit policy says otherwise

## 8.6 Table 14

### What can be filled now

- `planned_negative_rows` -> `120`
  action: insert direct package hard-negative denominator
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_closure_summary_v1.csv
- `tested_negative_rows` -> `111`
  action: insert direct tested denominator
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_closure_summary_v1.csv
- `NA_rows` -> `9`
  action: insert blocked / not-applicable count
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_closure_summary_v1.csv
- `executable_semantic_rejections` -> `111`
  action: insert executable mismatch rejection count
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_rejection_mode_audit_v1.csv
- `execution_failure_rejections` -> `0`
  action: insert negative execution failure rejection count
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_rejection_mode_audit_v1.csv
- `checker_failures` -> `0`
  action: insert checker failure count
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_rejection_mode_audit_v1.csv
- `false_accepts` -> `0`
  action: insert false accept count
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_rejection_mode_audit_v1.csv
- `per_pool_split_readiness` -> `pool rows retained in rejection-mode audit`
  action: use pool rows directly
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_rejection_mode_audit_v1.csv

### Claim boundary

- PERF/CONS/PORT/LONGTAIL rows already retained
- blocked not-applicable rows remain visible
- currently zero
- currently zero in retained packet
- do not hide blocked rows
- package hard-negative closure only
- package hard-negative false accepts only, not method accepted-candidate audit
- tested rows are semantic mismatches rather than crash rejections

## 8.6 Table 15

### What can be filled now

- `direct_llm / direct_llm_same_engine_rewrite planned` -> `120`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_same_engine_rewrite generation_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_same_engine_rewrite parse_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_same_engine_rewrite execution_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_same_engine_rewrite mismatch` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_same_engine_rewrite unsupported` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_same_engine_rewrite no-op` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_execute_repair_1shot planned` -> `120`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_execute_repair_1shot generation_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_execute_repair_1shot parse_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_execute_repair_1shot execution_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_execute_repair_1shot mismatch` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_execute_repair_1shot unsupported` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_execute_repair_1shot no-op` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop planned` -> `120`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop generation_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop parse_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop execution_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop mismatch` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop unsupported` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop no-op` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_optimize_same_dialect planned` -> `120`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_optimize_same_dialect generation_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_optimize_same_dialect parse_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_optimize_same_dialect execution_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_optimize_same_dialect mismatch` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_optimize_same_dialect unsupported` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_optimize_same_dialect no-op` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `calcite_hep / calcite_hep_fail_closed_120 planned` -> `120`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `calcite_hep / calcite_hep_fail_closed_120 generation_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `calcite_hep / calcite_hep_fail_closed_120 parse_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `calcite_hep / calcite_hep_fail_closed_120 execution_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `calcite_hep / calcite_hep_fail_closed_120 mismatch` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `calcite_hep / calcite_hep_fail_closed_120 unsupported` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `calcite_hep / calcite_hep_fail_closed_120 no-op` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_original_route_bounded_pg9 planned` -> `9`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_original_route_bounded_pg9 generation_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_original_route_bounded_pg9 parse_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_original_route_bounded_pg9 execution_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_original_route_bounded_pg9 mismatch` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_original_route_bounded_pg9 unsupported` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_original_route_bounded_pg9 no-op` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_recovered_extraction_route_v1 planned` -> `9`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_recovered_extraction_route_v1 generation_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_recovered_extraction_route_v1 parse_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_recovered_extraction_route_v1 execution_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_recovered_extraction_route_v1 mismatch` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_recovered_extraction_route_v1 unsupported` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_recovered_extraction_route_v1 no-op` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `r_bot / r_bot_same_engine_rewrite planned` -> `120`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `r_bot / r_bot_same_engine_rewrite generation_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `r_bot / r_bot_same_engine_rewrite parse_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `r_bot / r_bot_same_engine_rewrite execution_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `r_bot / r_bot_same_engine_rewrite mismatch` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `r_bot / r_bot_same_engine_rewrite unsupported` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `r_bot / r_bot_same_engine_rewrite no-op` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `learnedrewrite / UNKNOWN_NOT_RECOVERED planned` -> `10`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `learnedrewrite / UNKNOWN_NOT_RECOVERED generation_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `learnedrewrite / UNKNOWN_NOT_RECOVERED parse_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `learnedrewrite / UNKNOWN_NOT_RECOVERED execution_failed` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `learnedrewrite / UNKNOWN_NOT_RECOVERED mismatch` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `learnedrewrite / UNKNOWN_NOT_RECOVERED unsupported` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `learnedrewrite / UNKNOWN_NOT_RECOVERED no-op` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv

### What is computable from existing artifacts

- `direct_llm / direct_llm_same_engine_rewrite exact` -> `94`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_same_engine_rewrite non_exact` -> `26`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_execute_repair_1shot exact` -> `96`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `direct_llm / direct_llm_execute_repair_1shot non_exact` -> `24`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop exact` -> `72`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop non_exact` -> `48`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_optimize_same_dialect exact` -> `63`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `sqlglot / sqlglot_optimize_same_dialect non_exact` -> `57`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `calcite_hep / calcite_hep_fail_closed_120 exact` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `calcite_hep / calcite_hep_fail_closed_120 non_exact` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_original_route_bounded_pg9 exact` -> `3`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_original_route_bounded_pg9 non_exact` -> `6`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_recovered_extraction_route_v1 exact` -> `6`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `llm_r2 / llm_r2_recovered_extraction_route_v1 non_exact` -> `3`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `r_bot / r_bot_same_engine_rewrite exact` -> `NA_not_split`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `r_bot / r_bot_same_engine_rewrite non_exact` -> `NA_not_split`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `learnedrewrite / UNKNOWN_NOT_RECOVERED exact` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv
- `learnedrewrite / UNKNOWN_NOT_RECOVERED non_exact` -> `NA_not_found`
  action: route-level failure accounting field can be inserted or computed from retained failure matrix and rejection ledger
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table7_failure_accounting_matrix_v3.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/method_candidate_rejection_accounting_v1.csv

### Claim boundary

- do not conflate candidate rejection accounting with hard-negative rejection

## 8.7 Table 16

### What can be filled now

- `direct_llm / direct_llm_same_engine_rewrite timing denominator` -> `94`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_same_engine_rewrite GM` -> `1.043634242319266`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_same_engine_rewrite median` -> `1.009402551073825`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_same_engine_rewrite win` -> `22`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_same_engine_rewrite tie` -> `67`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_same_engine_rewrite loss` -> `5`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_same_engine_rewrite Regression@20` -> `0.03191489361702127`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_same_engine_rewrite best_case` -> `CONS_0012`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_same_engine_rewrite worst_case` -> `PERF_0007`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_execute_repair_1shot timing denominator` -> `96`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_execute_repair_1shot GM` -> `1.0430582867389244`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_execute_repair_1shot median` -> `1.009402551073825`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_execute_repair_1shot win` -> `23`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_execute_repair_1shot tie` -> `67`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_execute_repair_1shot loss` -> `6`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_execute_repair_1shot Regression@20` -> `0.041666666666666664`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_execute_repair_1shot best_case` -> `CONS_0012`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `direct_llm / direct_llm_execute_repair_1shot worst_case` -> `PERF_0007`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_optimize_same_dialect timing denominator` -> `63`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_optimize_same_dialect GM` -> `0.9907164888740984`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_optimize_same_dialect median` -> `0.9951145947521497`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_optimize_same_dialect win` -> `11`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_optimize_same_dialect tie` -> `37`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_optimize_same_dialect loss` -> `15`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_optimize_same_dialect Regression@20` -> `0.015873015873015872`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_optimize_same_dialect best_case` -> `PERF_0007`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_optimize_same_dialect worst_case` -> `CONS_0037`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop timing denominator` -> `72`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop GM` -> `1.000145903000493`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop median` -> `1.0020975938941747`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop win` -> `10`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop tie` -> `51`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop loss` -> `11`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop Regression@20` -> `0.013888888888888888`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop best_case` -> `LONGTAIL_0013`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_transpile_same_dialect_noop worst_case` -> `PERF_0062`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `calcite_hep / calcite_hep_fail_closed_120 timing denominator` -> `93`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `calcite_hep / calcite_hep_fail_closed_120 GM` -> `0.995917121478`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `calcite_hep / calcite_hep_fail_closed_120 median` -> `0.999279423532`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `calcite_hep / calcite_hep_fail_closed_120 win` -> `12`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `calcite_hep / calcite_hep_fail_closed_120 tie` -> `66`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `calcite_hep / calcite_hep_fail_closed_120 loss` -> `15`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `calcite_hep / calcite_hep_fail_closed_120 Regression@20` -> `0.0752688172043`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `calcite_hep / calcite_hep_fail_closed_120 best_case` -> `CONS_0011`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `calcite_hep / calcite_hep_fail_closed_120 worst_case` -> `PERF_0007`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `r_bot / r_bot_same_engine_rewrite timing denominator` -> `15`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `r_bot / r_bot_same_engine_rewrite GM` -> `0.9218248321470981`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `r_bot / r_bot_same_engine_rewrite median` -> `0.9820746516046041`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `r_bot / r_bot_same_engine_rewrite win` -> `1`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `r_bot / r_bot_same_engine_rewrite tie` -> `7`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `r_bot / r_bot_same_engine_rewrite loss` -> `7`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `r_bot / r_bot_same_engine_rewrite Regression@20` -> `0.2`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `r_bot / r_bot_same_engine_rewrite best_case` -> `CONS_0009`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `r_bot / r_bot_same_engine_rewrite worst_case` -> `CONS_0007`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_combined_same_engine_240 timing denominator` -> `137`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_combined_same_engine_240 GM` -> `1.0179`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_combined_same_engine_240 Regression@20` -> `0.0511`
  action: insert retained exact-timed summary value directly from Table 6
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv

### What requires aggregation

- `sqlglot / sqlglot_combined_same_engine_240 median` -> `needs_per_case_timing_aggregation`
  action: use retained timing summary or keep NA where the route is bounded-only
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_combined_same_engine_240 best_case` -> `needs_per_case_timing_aggregation`
  action: use retained timing summary or keep NA where the route is bounded-only
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_combined_same_engine_240 worst_case` -> `needs_per_case_timing_aggregation`
  action: use retained timing summary or keep NA where the route is bounded-only
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv

### What must stay NA / not computed

- `sqlglot / sqlglot_combined_same_engine_240 win` -> `NA_not_found`
  action: use retained timing summary or keep NA where the route is bounded-only
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_combined_same_engine_240 tie` -> `NA_not_found`
  action: use retained timing summary or keep NA where the route is bounded-only
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv
- `sqlglot / sqlglot_combined_same_engine_240 loss` -> `NA_not_found`
  action: use retained timing summary or keep NA where the route is bounded-only
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table6_performance_on_exact_timed_rows_v4.csv

### Claim boundary

- speedup valid only on exact plus timing-success rows

## 8.7 Table 17

### What can be filled now

- `case_id` -> `selected PG frontier row field retained in table10_plan_attribution_case_study_v6.csv`
  action: use retained selected-case plan attribution table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv
- `pool` -> `selected PG frontier row field retained in table10_plan_attribution_case_study_v6.csv`
  action: use retained selected-case plan attribution table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv
- `route` -> `selected PG frontier row field retained in table10_plan_attribution_case_study_v6.csv`
  action: use retained selected-case plan attribution table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv
- `engine` -> `selected PG frontier row field retained in table10_plan_attribution_case_study_v6.csv`
  action: use retained selected-case plan attribution table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv
- `outcome` -> `selected PG frontier row field retained in table10_plan_attribution_case_study_v6.csv`
  action: use retained selected-case plan attribution table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv
- `speedup` -> `selected PG frontier row field retained in table10_plan_attribution_case_study_v6.csv`
  action: use retained selected-case plan attribution table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv
- `delta_class` -> `selected PG frontier row field retained in table10_plan_attribution_case_study_v6.csv`
  action: use retained selected-case plan attribution table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv
- `confidence` -> `selected PG frontier row field retained in table10_plan_attribution_case_study_v6.csv`
  action: use retained selected-case plan attribution table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv
- `source_plan` -> `selected PG frontier row field retained in table10_plan_attribution_case_study_v6.csv`
  action: use retained selected-case plan attribution table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv
- `rewrite_plan` -> `selected PG frontier row field retained in table10_plan_attribution_case_study_v6.csv`
  action: use retained selected-case plan attribution table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv
- `notes` -> `selected PG frontier row field retained in table10_plan_attribution_case_study_v6.csv`
  action: use retained selected-case plan attribution table
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv

### Claim boundary

- selected PG plan attribution only; not denominator-wide causal attribution

## 8.8 Table 18

### What can be filled now

- `bounded PORT6 execution consistency closure` -> `bounded_port6_only`
  action: cite retained bounded closure packet only
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv

### What requires a new experiment

- `full PORT9 closure` -> `NA_not_computed`
  action: requires explicit PORT9 closure packet
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv
- `full PORT registry closure` -> `NA_not_computed`
  action: requires a broader registry-level portability packet
  source: inventory/case_registry.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv
- `target-engine paired timing evidence` -> `NA_not_found`
  action: needs retained paired target-engine exact timed transfer packet
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv

### What must stay NA / not computed

- `SpeedupTransferRate` -> `NA_not_computed`
  action: write NA / not computed
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv

### Claim boundary

- current evidence is bounded PORT6 only
- do not imply full registry closure from bounded packet
- must not be rewritten as full PORT9 or full PORT registry closure
- no retained paired timing arrays found
- requires paired target-engine timing arrays or repeated runtime summaries

## 8.9 Table 19

### What can be filled now

- `SQLSolver pair-level readiness` -> `smoke_only`
  action: insert bounded support status directly
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `SQLSolver denominator type` -> `support_pairs_4`
  action: insert direct pair denominator
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `SQLSolver support rate` -> `bounded_3_over_4_support_smoke`
  action: insert direct retained support-rate wording
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `VeriEQL pair-level readiness` -> `canary_only`
  action: insert bounded support status directly
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `VeriEQL denominator type` -> `cons_0035_pairs_2`
  action: insert direct pair denominator
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `VeriEQL support rate` -> `bounded_1.0_on_2_pairs_caveated`
  action: insert direct retained support-rate wording
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `VeriEQL prove` -> `0`
  action: use direct verifier table values or keep NA where not retained
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `VeriEQL refute` -> `2`
  action: use direct verifier table values or keep NA where not retained
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `VeriEQL unknown` -> `0`
  action: use direct verifier table values or keep NA where not retained
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `VeriEQL timeout` -> `0`
  action: use direct verifier table values or keep NA where not retained
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv

### What must stay NA / not computed

- `SQLSolver prove` -> `NA_not_found`
  action: use direct verifier table values or keep NA where not retained
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `SQLSolver refute` -> `NA_not_found`
  action: use direct verifier table values or keep NA where not retained
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `SQLSolver unknown` -> `NA_not_found`
  action: use direct verifier table values or keep NA where not retained
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
- `SQLSolver timeout` -> `NA_not_found`
  action: use direct verifier table values or keep NA where not retained
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv

### Claim boundary

- bounded support only
- do not place verifier support into same-engine speedup evidence
- keep support pairs separate from same-engine row denominator
- verifier support evidence only; not rewrite-generation baseline

## 8.10 Table 20

### What can be filled now

- `claim_01` -> `strong`
  action: map the conclusion to retained table support and keep forbidden overclaim boundary visible
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv
  notes: Do not describe the denominator as ad hoc or route-specific.
- `claim_03` -> `strong`
  action: map the conclusion to retained table support and keep forbidden overclaim boundary visible
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv
  notes: Do not compare speedup without first checking correctness scope.
- `claim_05` -> `strong`
  action: map the conclusion to retained table support and keep forbidden overclaim boundary visible
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv
  notes: Do not claim that the repair route is the same protocol as original Direct LLM or that it repaired the 5 blocked rows.
- `claim_09` -> `strong`
  action: map the conclusion to retained table support and keep forbidden overclaim boundary visible
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv
  notes: Do not reinterpret package-level hard-negative closure as method-generated candidate false-accept auditing.
- `claim_13` -> `strong`
  action: map the conclusion to retained table support and keep forbidden overclaim boundary visible
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv
  notes: Do not read Table 5 v6 as full 120 attribution, cross-engine attribution, or global causal attribution.
- `claim_14` -> `strong`
  action: map the conclusion to retained table support and keep forbidden overclaim boundary visible
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv
  notes: Do not claim denominator-wide causal attribution, full PlanParseRate, or cross-engine attribution from Table 10A v6.
- `claim_19` -> `strong`
  action: map the conclusion to retained table support and keep forbidden overclaim boundary visible
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv
  notes: Do not claim full PORT9 completion.
- `claim_20` -> `strong`
  action: map the conclusion to retained table support and keep forbidden overclaim boundary visible
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv
  notes: Do not report SpeedupTransferRate.
- `claim_21` -> `strong`
  action: map the conclusion to retained table support and keep forbidden overclaim boundary visible
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv
  notes: Do not compare SQLSolver or VeriEQL to rewrite methods on speedup or same-engine correctness tables.
- `claim_22` -> `strong`
  action: map the conclusion to retained table support and keep forbidden overclaim boundary visible
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_claim_matrix_v7.csv
  notes: Do not name a global winner or rank methods by GM speedup.

### Claim boundary

- this table should remain a conclusion-to-evidence map, not a new claim generator

## Appendix A Appendix A

### What can be filled now

- `common-core case list` -> `filled_from_existing_artifact`
  action: use retained artifact directly or build a new appendix render where needed
  source: reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table1_common_core_composition_v1.csv
  notes: common-core manifest plus composition table retained

### Claim boundary

- appendix-only readiness signal

## Appendix B Appendix B

### What requires aggregation

- `full 4+1 taxonomy tag matrix` -> `requires_new_aggregation`
  action: use retained artifact directly or build a new appendix render where needed
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_all_registry_cases_v1.csv
  notes: tag rows exist but appendix-specific matrix needs a new render

### Claim boundary

- appendix-only readiness signal

## Appendix C Appendix C

### What requires aggregation

- `taxonomy-aware failure slicing` -> `requires_new_aggregation`
  action: use retained artifact directly or build a new appendix render where needed
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/case_level_failure_export_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/tag_coverage_common_core40_v1.csv
  notes: join failure export to retained case tags

### Claim boundary

- appendix-only readiness signal

## Appendix D Appendix D

### What is computable from existing artifacts

- `hard-negative per-case per-engine ledger` -> `computable_from_existing_artifact`
  action: use retained artifact directly or build a new appendix render where needed
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/package_hard_negative_closure_event_long_v1.csv
  notes: per-row closure event_long already exists

### Claim boundary

- appendix-only readiness signal

## Appendix E Appendix E

### What can be filled now

- `route-level method cards` -> `filled_from_existing_artifact`
  action: use retained artifact directly or build a new appendix render where needed
  source: reports/evaluation/common_core_v0/direct_llm_same_engine_result_card_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/direct_llm_execute_repair_1shot_result_card_v1.csv|reports/evaluation/common_core_v0/sqlglot_transpile_same_dialect_noop_result_card_v1.csv|reports/evaluation/common_core_v0/sqlglot_optimize_same_dialect_result_card_v1.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/calcite_hep_93_exact_timing_result_card_v1.csv|reports/evaluation/common_core_v0/r_bot_formal_result_card_v1.csv
  notes: route-level cards already retained

### Claim boundary

- appendix-only readiness signal

## Appendix F Appendix F

### What can be filled now

- `selected plan observability frontier` -> `filled_from_existing_artifact`
  action: use retained artifact directly or build a new appendix render where needed
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table10_plan_attribution_case_study_v6.csv|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/pg_plan_attribution_113_summary_v1.csv
  notes: selected PG frontier and diagnostics retained

### Claim boundary

- appendix-only readiness signal

## Appendix G Appendix G

### What can be filled now

- `PORT bounded closure and SpeedupTransferRate readiness` -> `filled_from_existing_artifact`
  action: use retained artifact directly or build a new appendix render where needed
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table8_port_cross_engine_translation_v1.csv
  notes: bounded closure retained; SpeedupTransferRate remains NA

### Claim boundary

- appendix-only readiness signal

## Appendix H Appendix H

### What can be filled now

- `verifier support details` -> `filled_from_existing_artifact`
  action: use retained artifact directly or build a new appendix render where needed
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/table9_verifier_support_v1.csv
  notes: support details retained

### Claim boundary

- appendix-only readiness signal

## Appendix I Appendix I

### What requires manual review

- `reproducibility package` -> `requires_manual_review`
  action: use retained artifact directly or build a new appendix render where needed
  source: reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/common_core_v0_paper_results_readme_v10.md|reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/paper_results_table_index_v5.csv
  notes: retained freeze exists but appendix-specific reproducibility package scope needs human review

### Claim boundary

- appendix-only readiness signal
