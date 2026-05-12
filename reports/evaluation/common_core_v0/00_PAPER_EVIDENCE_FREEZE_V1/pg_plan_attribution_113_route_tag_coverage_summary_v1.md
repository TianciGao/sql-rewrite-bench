# PG Plan Attribution 113 Route Tag Coverage Summary V1

This file summarizes route x tag coverage after executing the 113-row PG frontier.
中文说明：后续 Table 5 v6 PREVIEW 应以这个 route x frontier x tag coverage 层为基础。

| method_id | route_id | planned_candidates | both_plan_success | ready_tag_count | observed_tag_count_after_success | recovered_common_core_missing_tags | missing_tag_after_execution | delta_class_distribution | attribution_confidence_distribution | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| calcite_hep | calcite_hep_fail_closed_120 | 31 | 31 | 48 | 48 | sql_feature:primary:subquery_in_from | none | aggregate_strategy_change:1\|buffer_or_runtime_delta_without_operator_change:25\|mixed_operator_change:1\|node_count_change:2\|scan_strategy_change:2 | low:26\|medium:5 |  |
| direct_llm | direct_llm_execute_repair_1shot | 2 | 2 | 17 | 17 | none | none | buffer_or_runtime_delta_without_operator_change:2 | low:2 |  |
| direct_llm | direct_llm_same_engine_rewrite | 32 | 32 | 56 | 56 | portability:confirmed:datetime_semantics_gap\|portability:confirmed:type_semantics_gap\|rewrite_opportunity:secondary:expression_simplification\|rewrite_opportunity:secondary:function_normalization\|sql_feature:primary:expression_complexity\|sql_feature:primary:subquery_in_from | none | buffer_or_runtime_delta_without_operator_change:30\|join_strategy_change:1\|mixed_operator_change:1 | low:30\|medium:2 |  |
| sqlglot | sqlglot_optimize_same_dialect | 22 | 22 | 55 | 55 | portability:confirmed:datetime_semantics_gap\|portability:confirmed:type_semantics_gap\|rewrite_opportunity:secondary:expression_simplification\|rewrite_opportunity:secondary:function_normalization\|sql_feature:primary:expression_complexity\|sql_feature:primary:subquery_in_from | none | buffer_or_runtime_delta_without_operator_change:17\|mixed_operator_change:4\|scan_strategy_change:1 | low:18\|medium:4 |  |
| sqlglot | sqlglot_transpile_same_dialect_noop | 26 | 26 | 48 | 48 | sql_feature:primary:subquery_in_from | none | buffer_or_runtime_delta_without_operator_change:26 | low:26 |  |
