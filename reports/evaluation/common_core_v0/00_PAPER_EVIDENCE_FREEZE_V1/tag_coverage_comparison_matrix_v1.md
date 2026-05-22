# Tag Coverage Comparison Matrix V1

- 这个文件回答什么问题：190 registry、40 common-core、24 selected PG attribution、113 PG-ready frontier、以及 Table 10 selected cases 之间的 tag coverage 差异。
- matrix 里同时保留 scope summaries、family frequency、tag frequency、pool x tag、route x tag。
- 这个比较用于决定是否值得扩展 PG attribution frontier。
- 没有运行任何新实验。

| scope_name | metric_type | dimension_family | dimension_value | pool_filter | method_route | numerator | denominator | coverage_rate | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all_registry_cases | scope_summary_total_rows |  |  |  |  | 190 |  |  | unique_cases=190 |
| all_registry_cases | scope_summary_tagged_rows |  |  |  |  | 189 | 190 | 0.994737 |  |
| all_registry_cases | scope_summary_missing_rows |  |  |  |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | family_frequency | plan_operator |  |  |  | 897 | 190 | 4.721053 |  |
| all_registry_cases | family_frequency | portability |  |  |  | 159 | 190 | 0.836842 |  |
| all_registry_cases | family_frequency | rewrite_opportunity |  |  |  | 357 | 190 | 1.878947 |  |
| all_registry_cases | family_frequency | sql_feature |  |  |  | 276 | 190 | 1.452632 |  |
| all_registry_cases | family_frequency | workload_realism |  |  |  | 306 | 190 | 1.610526 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  |  | 4 | 190 | 0.021053 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:delta_relevant:sort |  |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:present:aggregate |  |  | 163 | 190 | 0.857895 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:present:filter |  |  | 50 | 190 | 0.263158 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:present:join |  |  | 163 | 190 | 0.857895 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:present:limit |  |  | 61 | 190 | 0.321053 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:present:materialize |  |  | 51 | 190 | 0.268421 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:present:project |  |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:present:scan |  |  | 181 | 190 | 0.952632 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:present:set_op |  |  | 21 | 190 | 0.110526 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:present:sort |  |  | 107 | 190 | 0.563158 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:present:subquery |  |  | 64 | 190 | 0.336842 |  |
| all_registry_cases | tag_frequency | plan_operator | plan_operator:present:window |  |  | 21 | 190 | 0.110526 |  |
| all_registry_cases | tag_frequency | portability | portability:confirmed:boolean_semantics_gap |  |  | 8 | 190 | 0.042105 |  |
| all_registry_cases | tag_frequency | portability | portability:confirmed:datetime_semantics_gap |  |  | 11 | 190 | 0.057895 |  |
| all_registry_cases | tag_frequency | portability | portability:confirmed:engine_specific_syntax_gap |  |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | tag_frequency | portability | portability:confirmed:identifier_quoting |  |  | 26 | 190 | 0.136842 |  |
| all_registry_cases | tag_frequency | portability | portability:confirmed:limit_fetch_gap |  |  | 14 | 190 | 0.073684 |  |
| all_registry_cases | tag_frequency | portability | portability:confirmed:null_semantics_gap |  |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | tag_frequency | portability | portability:confirmed:type_semantics_gap |  |  | 14 | 190 | 0.073684 |  |
| all_registry_cases | tag_frequency | portability | portability:suspected:boolean_semantics_gap |  |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | tag_frequency | portability | portability:suspected:datetime_semantics_gap |  |  | 26 | 190 | 0.136842 |  |
| all_registry_cases | tag_frequency | portability | portability:suspected:engine_specific_syntax_gap |  |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | tag_frequency | portability | portability:suspected:null_semantics_gap |  |  | 19 | 190 | 0.100000 |  |
| all_registry_cases | tag_frequency | portability | portability:suspected:outer_join_support_gap |  |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | tag_frequency | portability | portability:suspected:set_operation_gap |  |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | tag_frequency | portability | portability:suspected:string_function_gap |  |  | 5 | 190 | 0.026316 |  |
| all_registry_cases | tag_frequency | portability | portability:suspected:type_semantics_gap |  |  | 19 | 190 | 0.100000 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite |  |  | 26 | 190 | 0.136842 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  |  | 17 | 190 | 0.089474 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:dialect_adaptation |  |  | 27 | 190 | 0.142105 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  |  | 35 | 190 | 0.184211 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy |  |  | 27 | 190 | 0.142105 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification |  |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  |  | 13 | 190 | 0.068421 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  |  | 41 | 190 | 0.215789 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  |  | 26 | 190 | 0.136842 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  |  | 21 | 190 | 0.110526 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:expression_simplification |  |  | 24 | 190 | 0.126316 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:function_normalization |  |  | 11 | 190 | 0.057895 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  |  | 7 | 190 | 0.036842 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  |  | 13 | 190 | 0.068421 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:order_limit_simplification |  |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  |  | 53 | 190 | 0.278947 |  |
| all_registry_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation |  |  | 3 | 190 | 0.015789 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  |  | 38 | 190 | 0.200000 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:primary:cte |  |  | 45 | 190 | 0.236842 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:primary:date_time_function |  |  | 31 | 190 | 0.163158 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:primary:expression_complexity |  |  | 26 | 190 | 0.136842 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:primary:non_equi_join |  |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:primary:outer_join |  |  | 21 | 190 | 0.110526 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:primary:set_operation |  |  | 21 | 190 | 0.110526 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:primary:string_function |  |  | 4 | 190 | 0.021053 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:primary:subquery_in_from |  |  | 18 | 190 | 0.094737 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:primary:window_function |  |  | 22 | 190 | 0.115789 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:secondary:date_time_function |  |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  |  | 19 | 190 | 0.100000 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:secondary:outer_join |  |  | 11 | 190 | 0.057895 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:secondary:string_function |  |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  |  | 16 | 190 | 0.084211 |  |
| all_registry_cases | tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  |  | 32 | 190 | 0.168421 |  |
| all_registry_cases | tag_frequency | workload_realism | workload_realism:case_specific:high_join_count |  |  | 32 | 190 | 0.168421 |  |
| all_registry_cases | tag_frequency | workload_realism | workload_realism:case_specific:long_query_text |  |  | 20 | 190 | 0.105263 |  |
| all_registry_cases | tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  |  | 26 | 190 | 0.136842 |  |
| all_registry_cases | tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity |  |  | 18 | 190 | 0.094737 |  |
| all_registry_cases | tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  |  | 98 | 190 | 0.515789 |  |
| all_registry_cases | tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  |  | 6 | 190 | 0.031579 |  |
| all_registry_cases | tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  |  | 25 | 190 | 0.131579 |  |
| all_registry_cases | tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  |  | 49 | 190 | 0.257895 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | consistency |  | 27 | 190 | 0.142105 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:join | consistency |  | 29 | 190 | 0.152632 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:limit | consistency |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:materialize | consistency |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:project | consistency |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:scan | consistency |  | 36 | 190 | 0.189474 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:set_op | consistency |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:sort | consistency |  | 6 | 190 | 0.031579 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:subquery | consistency |  | 30 | 190 | 0.157895 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:confirmed:boolean_semantics_gap | consistency |  | 3 | 190 | 0.015789 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | consistency |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:confirmed:null_semantics_gap | consistency |  | 9 | 190 | 0.047368 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:null_semantics_gap | consistency |  | 5 | 190 | 0.026316 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite | consistency |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification | consistency |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation | consistency |  | 29 | 190 | 0.152632 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite | consistency |  | 7 | 190 | 0.036842 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:expression_simplification | consistency |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy | consistency |  | 4 | 190 | 0.021053 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown | consistency |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation | consistency |  | 3 | 190 | 0.015789 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery | consistency |  | 26 | 190 | 0.136842 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:expression_complexity | consistency |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:non_equi_join | consistency |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | consistency |  | 9 | 190 | 0.047368 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:set_operation | consistency |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:subquery_in_from | consistency |  | 5 | 190 | 0.026316 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from | consistency |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | consistency |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | consistency |  | 3 | 190 | 0.015789 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism | consistency |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | longtail |  | 20 | 190 | 0.105263 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:join | longtail |  | 20 | 190 | 0.105263 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:limit | longtail |  | 3 | 190 | 0.015789 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:materialize | longtail |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:scan | longtail |  | 20 | 190 | 0.105263 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:sort | longtail |  | 20 | 190 | 0.105263 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:subquery | longtail |  | 18 | 190 | 0.094737 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:window | longtail |  | 12 | 190 | 0.063158 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:datetime_semantics_gap | longtail |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:null_semantics_gap | longtail |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite | longtail |  | 3 | 190 | 0.015789 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy | longtail |  | 17 | 190 | 0.089474 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification | longtail |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy | longtail |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite | longtail |  | 17 | 190 | 0.089474 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy | longtail |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy | longtail |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:cte | longtail |  | 18 | 190 | 0.094737 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:expression_complexity | longtail |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | longtail |  | 7 | 190 | 0.036842 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:subquery_in_from | longtail |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:window_function | longtail |  | 13 | 190 | 0.068421 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | longtail |  | 11 | 190 | 0.057895 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:secondary:outer_join | longtail |  | 11 | 190 | 0.057895 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | longtail |  | 9 | 190 | 0.047368 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count | longtail |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | longtail |  | 5 | 190 | 0.026316 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity | longtail |  | 9 | 190 | 0.047368 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism | longtail |  | 4 | 190 | 0.021053 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style | longtail |  | 21 | 190 | 0.110526 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize | performance |  | 4 | 190 | 0.021053 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:delta_relevant:sort | performance |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | performance |  | 100 | 190 | 0.526316 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:filter | performance |  | 28 | 190 | 0.147368 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:join | performance |  | 97 | 190 | 0.510526 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:limit | performance |  | 47 | 190 | 0.247368 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:materialize | performance |  | 39 | 190 | 0.205263 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:scan | performance |  | 100 | 190 | 0.526316 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:set_op | performance |  | 19 | 190 | 0.100000 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:sort | performance |  | 69 | 190 | 0.363158 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:subquery | performance |  | 15 | 190 | 0.078947 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:window | performance |  | 9 | 190 | 0.047368 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | performance |  | 3 | 190 | 0.015789 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:datetime_semantics_gap | performance |  | 25 | 190 | 0.131579 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:engine_specific_syntax_gap | performance |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:null_semantics_gap | performance |  | 9 | 190 | 0.047368 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:outer_join_support_gap | performance |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:set_operation_gap | performance |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:string_function_gap | performance |  | 5 | 190 | 0.026316 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:type_semantics_gap | performance |  | 19 | 190 | 0.100000 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite | performance |  | 13 | 190 | 0.068421 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification | performance |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder | performance |  | 35 | 190 | 0.184211 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy | performance |  | 26 | 190 | 0.136842 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown | performance |  | 13 | 190 | 0.068421 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation | performance |  | 12 | 190 | 0.063158 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite | performance |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy | performance |  | 20 | 190 | 0.105263 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:expression_simplification | performance |  | 9 | 190 | 0.047368 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:function_normalization | performance |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder | performance |  | 7 | 190 | 0.036842 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy | performance |  | 8 | 190 | 0.042105 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown | performance |  | 52 | 190 | 0.273684 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery | performance |  | 12 | 190 | 0.063158 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:cte | performance |  | 27 | 190 | 0.142105 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:date_time_function | performance |  | 21 | 190 | 0.110526 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:expression_complexity | performance |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | performance |  | 5 | 190 | 0.026316 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:set_operation | performance |  | 19 | 190 | 0.100000 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:string_function | performance |  | 4 | 190 | 0.021053 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:subquery_in_from | performance |  | 11 | 190 | 0.057895 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:window_function | performance |  | 9 | 190 | 0.047368 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:secondary:date_time_function | performance |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | performance |  | 7 | 190 | 0.036842 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:secondary:string_function | performance |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from | performance |  | 14 | 190 | 0.073684 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | performance |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count | performance |  | 30 | 190 | 0.157895 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_query_text | performance |  | 20 | 190 | 0.105263 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | performance |  | 17 | 190 | 0.089474 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline | performance |  | 98 | 190 | 0.515789 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation | performance |  | 25 | 190 | 0.131579 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style | performance |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | portability |  | 16 | 190 | 0.084211 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:filter | portability |  | 22 | 190 | 0.115789 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:join | portability |  | 17 | 190 | 0.089474 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:limit | portability |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:scan | portability |  | 25 | 190 | 0.131579 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:sort | portability |  | 12 | 190 | 0.063158 |  |
| all_registry_cases | pool_tag_frequency | plan_operator | plan_operator:present:subquery | portability |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:confirmed:boolean_semantics_gap | portability |  | 5 | 190 | 0.026316 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:confirmed:datetime_semantics_gap | portability |  | 11 | 190 | 0.057895 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:confirmed:engine_specific_syntax_gap | portability |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:confirmed:identifier_quoting | portability |  | 26 | 190 | 0.136842 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | portability |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:confirmed:null_semantics_gap | portability |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:confirmed:type_semantics_gap | portability |  | 14 | 190 | 0.073684 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:boolean_semantics_gap | portability |  | 2 | 190 | 0.010526 |  |
| all_registry_cases | pool_tag_frequency | portability | portability:suspected:null_semantics_gap | portability |  | 4 | 190 | 0.021053 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:dialect_adaptation | portability |  | 27 | 190 | 0.142105 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:expression_simplification | portability |  | 13 | 190 | 0.068421 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:function_normalization | portability |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:order_limit_simplification | portability |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:date_time_function | portability |  | 10 | 190 | 0.052632 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:primary:expression_complexity | portability |  | 13 | 190 | 0.068421 |  |
| all_registry_cases | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | portability |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | portability |  | 11 | 190 | 0.057895 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | portability |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity | portability |  | 9 | 190 | 0.047368 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism | portability |  | 1 | 190 | 0.005263 |  |
| all_registry_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style | portability |  | 26 | 190 | 0.136842 |  |
| common_core40 | scope_summary_total_rows |  |  |  |  | 40 |  |  | unique_cases=40 |
| common_core40 | scope_summary_tagged_rows |  |  |  |  | 40 | 40 | 1.000000 |  |
| common_core40 | scope_summary_missing_rows |  |  |  |  | 0 | 40 | 0.000000 |  |
| common_core40 | family_frequency | plan_operator |  |  |  | 178 | 40 | 4.450000 |  |
| common_core40 | family_frequency | portability |  |  |  | 44 | 40 | 1.100000 |  |
| common_core40 | family_frequency | rewrite_opportunity |  |  |  | 79 | 40 | 1.975000 |  |
| common_core40 | family_frequency | sql_feature |  |  |  | 58 | 40 | 1.450000 |  |
| common_core40 | family_frequency | workload_realism |  |  |  | 54 | 40 | 1.350000 |  |
| common_core40 | tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  |  | 1 | 40 | 0.025000 |  |
| common_core40 | tag_frequency | plan_operator | plan_operator:present:aggregate |  |  | 34 | 40 | 0.850000 |  |
| common_core40 | tag_frequency | plan_operator | plan_operator:present:filter |  |  | 9 | 40 | 0.225000 |  |
| common_core40 | tag_frequency | plan_operator | plan_operator:present:join |  |  | 32 | 40 | 0.800000 |  |
| common_core40 | tag_frequency | plan_operator | plan_operator:present:limit |  |  | 13 | 40 | 0.325000 |  |
| common_core40 | tag_frequency | plan_operator | plan_operator:present:materialize |  |  | 7 | 40 | 0.175000 |  |
| common_core40 | tag_frequency | plan_operator | plan_operator:present:scan |  |  | 40 | 40 | 1.000000 |  |
| common_core40 | tag_frequency | plan_operator | plan_operator:present:set_op |  |  | 2 | 40 | 0.050000 |  |
| common_core40 | tag_frequency | plan_operator | plan_operator:present:sort |  |  | 23 | 40 | 0.575000 |  |
| common_core40 | tag_frequency | plan_operator | plan_operator:present:subquery |  |  | 13 | 40 | 0.325000 |  |
| common_core40 | tag_frequency | plan_operator | plan_operator:present:window |  |  | 4 | 40 | 0.100000 |  |
| common_core40 | tag_frequency | portability | portability:confirmed:boolean_semantics_gap |  |  | 2 | 40 | 0.050000 |  |
| common_core40 | tag_frequency | portability | portability:confirmed:datetime_semantics_gap |  |  | 5 | 40 | 0.125000 |  |
| common_core40 | tag_frequency | portability | portability:confirmed:identifier_quoting |  |  | 9 | 40 | 0.225000 |  |
| common_core40 | tag_frequency | portability | portability:confirmed:limit_fetch_gap |  |  | 6 | 40 | 0.150000 |  |
| common_core40 | tag_frequency | portability | portability:confirmed:null_semantics_gap |  |  | 3 | 40 | 0.075000 |  |
| common_core40 | tag_frequency | portability | portability:confirmed:type_semantics_gap |  |  | 6 | 40 | 0.150000 |  |
| common_core40 | tag_frequency | portability | portability:suspected:datetime_semantics_gap |  |  | 7 | 40 | 0.175000 |  |
| common_core40 | tag_frequency | portability | portability:suspected:null_semantics_gap |  |  | 3 | 40 | 0.075000 |  |
| common_core40 | tag_frequency | portability | portability:suspected:type_semantics_gap |  |  | 3 | 40 | 0.075000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite |  |  | 3 | 40 | 0.075000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  |  | 4 | 40 | 0.100000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:dialect_adaptation |  |  | 9 | 40 | 0.225000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  |  | 1 | 40 | 0.025000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  |  | 3 | 40 | 0.075000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy |  |  | 3 | 40 | 0.075000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification |  |  | 1 | 40 | 0.025000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  |  | 7 | 40 | 0.175000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  |  | 9 | 40 | 0.225000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  |  | 7 | 40 | 0.175000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  |  | 3 | 40 | 0.075000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:expression_simplification |  |  | 4 | 40 | 0.100000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:function_normalization |  |  | 5 | 40 | 0.125000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  |  | 4 | 40 | 0.100000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  |  | 4 | 40 | 0.100000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:order_limit_simplification |  |  | 3 | 40 | 0.075000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  |  | 8 | 40 | 0.200000 |  |
| common_core40 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation |  |  | 1 | 40 | 0.025000 |  |
| common_core40 | tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  |  | 10 | 40 | 0.250000 |  |
| common_core40 | tag_frequency | sql_feature | sql_feature:primary:cte |  |  | 8 | 40 | 0.200000 |  |
| common_core40 | tag_frequency | sql_feature | sql_feature:primary:date_time_function |  |  | 11 | 40 | 0.275000 |  |
| common_core40 | tag_frequency | sql_feature | sql_feature:primary:expression_complexity |  |  | 4 | 40 | 0.100000 |  |
| common_core40 | tag_frequency | sql_feature | sql_feature:primary:outer_join |  |  | 6 | 40 | 0.150000 |  |
| common_core40 | tag_frequency | sql_feature | sql_feature:primary:set_operation |  |  | 2 | 40 | 0.050000 |  |
| common_core40 | tag_frequency | sql_feature | sql_feature:primary:subquery_in_from |  |  | 2 | 40 | 0.050000 |  |
| common_core40 | tag_frequency | sql_feature | sql_feature:primary:window_function |  |  | 4 | 40 | 0.100000 |  |
| common_core40 | tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  |  | 6 | 40 | 0.150000 |  |
| common_core40 | tag_frequency | sql_feature | sql_feature:secondary:outer_join |  |  | 2 | 40 | 0.050000 |  |
| common_core40 | tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  |  | 3 | 40 | 0.075000 |  |
| common_core40 | tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  |  | 7 | 40 | 0.175000 |  |
| common_core40 | tag_frequency | workload_realism | workload_realism:case_specific:high_join_count |  |  | 1 | 40 | 0.025000 |  |
| common_core40 | tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  |  | 6 | 40 | 0.150000 |  |
| common_core40 | tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity |  |  | 4 | 40 | 0.100000 |  |
| common_core40 | tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  |  | 16 | 40 | 0.400000 |  |
| common_core40 | tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  |  | 3 | 40 | 0.075000 |  |
| common_core40 | tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  |  | 2 | 40 | 0.050000 |  |
| common_core40 | tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  |  | 15 | 40 | 0.375000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | consistency |  | 7 | 40 | 0.175000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:join | consistency |  | 8 | 40 | 0.200000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:limit | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:materialize | consistency |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:scan | consistency |  | 9 | 40 | 0.225000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:set_op | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:sort | consistency |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:subquery | consistency |  | 7 | 40 | 0.175000 |  |
| common_core40 | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | portability | portability:confirmed:null_semantics_gap | consistency |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | portability | portability:suspected:null_semantics_gap | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite | consistency |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation | consistency |  | 6 | 40 | 0.150000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite | consistency |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery | consistency |  | 7 | 40 | 0.175000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | consistency |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:set_operation | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:subquery_in_from | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | consistency |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | longtail |  | 6 | 40 | 0.150000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:join | longtail |  | 6 | 40 | 0.150000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:limit | longtail |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:materialize | longtail |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:scan | longtail |  | 6 | 40 | 0.150000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:sort | longtail |  | 6 | 40 | 0.150000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:subquery | longtail |  | 6 | 40 | 0.150000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:window | longtail |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | portability | portability:suspected:datetime_semantics_gap | longtail |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | portability | portability:suspected:null_semantics_gap | longtail |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy | longtail |  | 4 | 40 | 0.100000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification | longtail |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy | longtail |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite | longtail |  | 5 | 40 | 0.125000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy | longtail |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:cte | longtail |  | 5 | 40 | 0.125000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | longtail |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:subquery_in_from | longtail |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:window_function | longtail |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | longtail |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:secondary:outer_join | longtail |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | longtail |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count | longtail |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | longtail |  | 4 | 40 | 0.100000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity | longtail |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism | longtail |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style | longtail |  | 6 | 40 | 0.150000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize | performance |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | performance |  | 16 | 40 | 0.400000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:filter | performance |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:join | performance |  | 14 | 40 | 0.350000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:limit | performance |  | 8 | 40 | 0.200000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:materialize | performance |  | 4 | 40 | 0.100000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:scan | performance |  | 16 | 40 | 0.400000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:set_op | performance |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:sort | performance |  | 12 | 40 | 0.300000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:window | performance |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | performance |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | portability | portability:suspected:datetime_semantics_gap | performance |  | 6 | 40 | 0.150000 |  |
| common_core40 | pool_tag_frequency | portability | portability:suspected:type_semantics_gap | performance |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite | performance |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder | performance |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy | performance |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown | performance |  | 7 | 40 | 0.175000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation | performance |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy | performance |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder | performance |  | 4 | 40 | 0.100000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy | performance |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown | performance |  | 7 | 40 | 0.175000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery | performance |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:cte | performance |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:date_time_function | performance |  | 6 | 40 | 0.150000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | performance |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:set_operation | performance |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:window_function | performance |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | performance |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from | performance |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | performance |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | performance |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline | performance |  | 16 | 40 | 0.400000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation | performance |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | portability |  | 5 | 40 | 0.125000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:filter | portability |  | 7 | 40 | 0.175000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:join | portability |  | 4 | 40 | 0.100000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:limit | portability |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:scan | portability |  | 9 | 40 | 0.225000 |  |
| common_core40 | pool_tag_frequency | plan_operator | plan_operator:present:sort | portability |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | portability | portability:confirmed:boolean_semantics_gap | portability |  | 2 | 40 | 0.050000 |  |
| common_core40 | pool_tag_frequency | portability | portability:confirmed:datetime_semantics_gap | portability |  | 5 | 40 | 0.125000 |  |
| common_core40 | pool_tag_frequency | portability | portability:confirmed:identifier_quoting | portability |  | 9 | 40 | 0.225000 |  |
| common_core40 | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | portability |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | portability | portability:confirmed:null_semantics_gap | portability |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | portability | portability:confirmed:type_semantics_gap | portability |  | 6 | 40 | 0.150000 |  |
| common_core40 | pool_tag_frequency | portability | portability:suspected:null_semantics_gap | portability |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:dialect_adaptation | portability |  | 9 | 40 | 0.225000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:expression_simplification | portability |  | 4 | 40 | 0.100000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:function_normalization | portability |  | 5 | 40 | 0.125000 |  |
| common_core40 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:order_limit_simplification | portability |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:date_time_function | portability |  | 5 | 40 | 0.125000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:primary:expression_complexity | portability |  | 4 | 40 | 0.100000 |  |
| common_core40 | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | portability |  | 1 | 40 | 0.025000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | portability |  | 4 | 40 | 0.100000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity | portability |  | 3 | 40 | 0.075000 |  |
| common_core40 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style | portability |  | 9 | 40 | 0.225000 |  |
| pg_attribution_24 | scope_summary_total_rows |  |  |  |  | 24 |  |  | unique_cases=20 |
| pg_attribution_24 | scope_summary_tagged_rows |  |  |  |  | 24 | 24 | 1.000000 |  |
| pg_attribution_24 | scope_summary_missing_rows |  |  |  |  | 0 | 24 | 0.000000 |  |
| pg_attribution_24 | family_frequency | plan_operator |  |  |  | 115 | 24 | 4.791667 |  |
| pg_attribution_24 | family_frequency | portability |  |  |  | 17 | 24 | 0.708333 |  |
| pg_attribution_24 | family_frequency | rewrite_opportunity |  |  |  | 44 | 24 | 1.833333 |  |
| pg_attribution_24 | family_frequency | sql_feature |  |  |  | 35 | 24 | 1.458333 |  |
| pg_attribution_24 | family_frequency | workload_realism |  |  |  | 31 | 24 | 1.291667 |  |
| pg_attribution_24 | tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | tag_frequency | plan_operator | plan_operator:present:aggregate |  |  | 21 | 24 | 0.875000 |  |
| pg_attribution_24 | tag_frequency | plan_operator | plan_operator:present:filter |  |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | tag_frequency | plan_operator | plan_operator:present:join |  |  | 21 | 24 | 0.875000 |  |
| pg_attribution_24 | tag_frequency | plan_operator | plan_operator:present:limit |  |  | 7 | 24 | 0.291667 |  |
| pg_attribution_24 | tag_frequency | plan_operator | plan_operator:present:materialize |  |  | 7 | 24 | 0.291667 |  |
| pg_attribution_24 | tag_frequency | plan_operator | plan_operator:present:scan |  |  | 24 | 24 | 1.000000 |  |
| pg_attribution_24 | tag_frequency | plan_operator | plan_operator:present:set_op |  |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | tag_frequency | plan_operator | plan_operator:present:sort |  |  | 17 | 24 | 0.708333 |  |
| pg_attribution_24 | tag_frequency | plan_operator | plan_operator:present:subquery |  |  | 9 | 24 | 0.375000 |  |
| pg_attribution_24 | tag_frequency | plan_operator | plan_operator:present:window |  |  | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | tag_frequency | portability | portability:confirmed:identifier_quoting |  |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | tag_frequency | portability | portability:confirmed:limit_fetch_gap |  |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | tag_frequency | portability | portability:confirmed:null_semantics_gap |  |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | tag_frequency | portability | portability:suspected:datetime_semantics_gap |  |  | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | tag_frequency | portability | portability:suspected:null_semantics_gap |  |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | tag_frequency | portability | portability:suspected:type_semantics_gap |  |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite |  |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:dialect_adaptation |  |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy |  |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification |  |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  |  | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  |  | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:order_limit_simplification |  |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  |  | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation |  |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | tag_frequency | sql_feature | sql_feature:primary:cte |  |  | 7 | 24 | 0.291667 |  |
| pg_attribution_24 | tag_frequency | sql_feature | sql_feature:primary:date_time_function |  |  | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | tag_frequency | sql_feature | sql_feature:primary:outer_join |  |  | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | tag_frequency | sql_feature | sql_feature:primary:set_operation |  |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | tag_frequency | sql_feature | sql_feature:primary:window_function |  |  | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | tag_frequency | sql_feature | sql_feature:secondary:outer_join |  |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | tag_frequency | workload_realism | workload_realism:case_specific:high_join_count |  |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity |  |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  |  | 12 | 24 | 0.500000 |  |
| pg_attribution_24 | tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  |  | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | consistency |  | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:join | consistency |  | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:limit | consistency |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:materialize | consistency |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:scan | consistency |  | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:sort | consistency |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:subquery | consistency |  | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | consistency |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | portability | portability:confirmed:null_semantics_gap | consistency |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite | consistency |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification | consistency |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation | consistency |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite | consistency |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation | consistency |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery | consistency |  | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | consistency |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | longtail |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:join | longtail |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:materialize | longtail |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:scan | longtail |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:sort | longtail |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:subquery | longtail |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:window | longtail |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | pool_tag_frequency | portability | portability:suspected:null_semantics_gap | longtail |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy | longtail |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification | longtail |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite | longtail |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy | longtail |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:primary:cte | longtail |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | longtail |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:primary:window_function | longtail |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | longtail |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:secondary:outer_join | longtail |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | longtail |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count | longtail |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | longtail |  | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism | longtail |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style | longtail |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize | performance |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | performance |  | 12 | 24 | 0.500000 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:filter | performance |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:join | performance |  | 10 | 24 | 0.416667 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:limit | performance |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:materialize | performance |  | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:scan | performance |  | 12 | 24 | 0.500000 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:set_op | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:sort | performance |  | 8 | 24 | 0.333333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:window | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | portability | portability:suspected:datetime_semantics_gap | performance |  | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | pool_tag_frequency | portability | portability:suspected:type_semantics_gap | performance |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder | performance |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy | performance |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown | performance |  | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder | performance |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy | performance |  | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown | performance |  | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:primary:cte | performance |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:primary:date_time_function | performance |  | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:primary:set_operation | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:primary:window_function | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from | performance |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | performance |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline | performance |  | 12 | 24 | 0.500000 |  |
| pg_attribution_24 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation | performance |  | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:limit | portability |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:scan | portability |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | plan_operator | plan_operator:present:sort | portability |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | portability | portability:confirmed:identifier_quoting | portability |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | portability |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | portability | portability:confirmed:null_semantics_gap | portability |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:dialect_adaptation | portability |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:order_limit_simplification | portability |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity | portability |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style | portability |  | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | calcite_hep / calcite_hep_fail_closed_120 | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:join |  | calcite_hep / calcite_hep_fail_closed_120 | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:limit |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:materialize |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:scan |  | calcite_hep / calcite_hep_fail_closed_120 | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:sort |  | calcite_hep / calcite_hep_fail_closed_120 | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:window |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:confirmed:limit_fetch_gap |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:confirmed:null_semantics_gap |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:suspected:datetime_semantics_gap |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:suspected:type_semantics_gap |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:date_time_function |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:outer_join |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:window_function |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:secondary:outer_join |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | calcite_hep / calcite_hep_fail_closed_120 | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | direct_llm / direct_llm_execute_repair_1shot | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:join |  | direct_llm / direct_llm_execute_repair_1shot | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:scan |  | direct_llm / direct_llm_execute_repair_1shot | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:sort |  | direct_llm / direct_llm_execute_repair_1shot | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:outer_join |  | direct_llm / direct_llm_execute_repair_1shot | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | direct_llm / direct_llm_same_engine_rewrite | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:join |  | direct_llm / direct_llm_same_engine_rewrite | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:limit |  | direct_llm / direct_llm_same_engine_rewrite | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:scan |  | direct_llm / direct_llm_same_engine_rewrite | 6 | 24 | 0.250000 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:set_op |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:sort |  | direct_llm / direct_llm_same_engine_rewrite | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:confirmed:identifier_quoting |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:confirmed:limit_fetch_gap |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:confirmed:null_semantics_gap |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:suspected:datetime_semantics_gap |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:suspected:type_semantics_gap |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:dialect_adaptation |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:order_limit_simplification |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:date_time_function |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:outer_join |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:set_operation |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | direct_llm / direct_llm_same_engine_rewrite | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | sqlglot / sqlglot_optimize_same_dialect | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:filter |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:join |  | sqlglot / sqlglot_optimize_same_dialect | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:materialize |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:scan |  | sqlglot / sqlglot_optimize_same_dialect | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:sort |  | sqlglot / sqlglot_optimize_same_dialect | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | sqlglot / sqlglot_optimize_same_dialect | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:window |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:suspected:null_semantics_gap |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:outer_join |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:window_function |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | sqlglot / sqlglot_transpile_same_dialect_noop | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:filter |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:join |  | sqlglot / sqlglot_transpile_same_dialect_noop | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:limit |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:materialize |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:scan |  | sqlglot / sqlglot_transpile_same_dialect_noop | 5 | 24 | 0.208333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:sort |  | sqlglot / sqlglot_transpile_same_dialect_noop | 4 | 24 | 0.166667 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | plan_operator | plan_operator:present:window |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:confirmed:null_semantics_gap |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:suspected:datetime_semantics_gap |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | portability | portability:suspected:type_semantics_gap |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:date_time_function |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:primary:window_function |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 24 | 0.083333 |  |
| pg_attribution_24 | route_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | sqlglot / sqlglot_transpile_same_dialect_noop | 3 | 24 | 0.125000 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_24 | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 24 | 0.041667 |  |
| pg_attribution_ready_113 | scope_summary_total_rows |  |  |  |  | 113 |  |  | unique_cases=35 |
| pg_attribution_ready_113 | scope_summary_tagged_rows |  |  |  |  | 113 | 113 | 1.000000 |  |
| pg_attribution_ready_113 | scope_summary_missing_rows |  |  |  |  | 0 | 113 | 0.000000 |  |
| pg_attribution_ready_113 | family_frequency | plan_operator |  |  |  | 535 | 113 | 4.734513 |  |
| pg_attribution_ready_113 | family_frequency | portability |  |  |  | 78 | 113 | 0.690265 |  |
| pg_attribution_ready_113 | family_frequency | rewrite_opportunity |  |  |  | 216 | 113 | 1.911504 |  |
| pg_attribution_ready_113 | family_frequency | sql_feature |  |  |  | 178 | 113 | 1.575221 |  |
| pg_attribution_ready_113 | family_frequency | workload_realism |  |  |  | 152 | 113 | 1.345133 |  |
| pg_attribution_ready_113 | tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | tag_frequency | plan_operator | plan_operator:present:aggregate |  |  | 101 | 113 | 0.893805 |  |
| pg_attribution_ready_113 | tag_frequency | plan_operator | plan_operator:present:filter |  |  | 14 | 113 | 0.123894 |  |
| pg_attribution_ready_113 | tag_frequency | plan_operator | plan_operator:present:join |  |  | 98 | 113 | 0.867257 |  |
| pg_attribution_ready_113 | tag_frequency | plan_operator | plan_operator:present:limit |  |  | 37 | 113 | 0.327434 |  |
| pg_attribution_ready_113 | tag_frequency | plan_operator | plan_operator:present:materialize |  |  | 26 | 113 | 0.230088 |  |
| pg_attribution_ready_113 | tag_frequency | plan_operator | plan_operator:present:scan |  |  | 113 | 113 | 1.000000 |  |
| pg_attribution_ready_113 | tag_frequency | plan_operator | plan_operator:present:set_op |  |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | tag_frequency | plan_operator | plan_operator:present:sort |  |  | 72 | 113 | 0.637168 |  |
| pg_attribution_ready_113 | tag_frequency | plan_operator | plan_operator:present:subquery |  |  | 47 | 113 | 0.415929 |  |
| pg_attribution_ready_113 | tag_frequency | plan_operator | plan_operator:present:window |  |  | 16 | 113 | 0.141593 |  |
| pg_attribution_ready_113 | tag_frequency | portability | portability:confirmed:datetime_semantics_gap |  |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | tag_frequency | portability | portability:confirmed:identifier_quoting |  |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | tag_frequency | portability | portability:confirmed:limit_fetch_gap |  |  | 12 | 113 | 0.106195 |  |
| pg_attribution_ready_113 | tag_frequency | portability | portability:confirmed:null_semantics_gap |  |  | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | tag_frequency | portability | portability:confirmed:type_semantics_gap |  |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | tag_frequency | portability | portability:suspected:datetime_semantics_gap |  |  | 23 | 113 | 0.203540 |  |
| pg_attribution_ready_113 | tag_frequency | portability | portability:suspected:null_semantics_gap |  |  | 9 | 113 | 0.079646 |  |
| pg_attribution_ready_113 | tag_frequency | portability | portability:suspected:type_semantics_gap |  |  | 11 | 113 | 0.097345 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite |  |  | 10 | 113 | 0.088496 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  |  | 16 | 113 | 0.141593 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:dialect_adaptation |  |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  |  | 10 | 113 | 0.088496 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy |  |  | 11 | 113 | 0.097345 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification |  |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  |  | 22 | 113 | 0.194690 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  |  | 29 | 113 | 0.256637 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  |  | 27 | 113 | 0.238938 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  |  | 11 | 113 | 0.097345 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:expression_simplification |  |  | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:function_normalization |  |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  |  | 12 | 113 | 0.106195 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  |  | 13 | 113 | 0.115044 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:order_limit_simplification |  |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  |  | 27 | 113 | 0.238938 |  |
| pg_attribution_ready_113 | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation |  |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  |  | 33 | 113 | 0.292035 |  |
| pg_attribution_ready_113 | tag_frequency | sql_feature | sql_feature:primary:cte |  |  | 31 | 113 | 0.274336 |  |
| pg_attribution_ready_113 | tag_frequency | sql_feature | sql_feature:primary:date_time_function |  |  | 23 | 113 | 0.203540 |  |
| pg_attribution_ready_113 | tag_frequency | sql_feature | sql_feature:primary:expression_complexity |  |  | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | tag_frequency | sql_feature | sql_feature:primary:outer_join |  |  | 20 | 113 | 0.176991 |  |
| pg_attribution_ready_113 | tag_frequency | sql_feature | sql_feature:primary:set_operation |  |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | tag_frequency | sql_feature | sql_feature:primary:subquery_in_from |  |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | tag_frequency | sql_feature | sql_feature:primary:window_function |  |  | 16 | 113 | 0.141593 |  |
| pg_attribution_ready_113 | tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  |  | 22 | 113 | 0.194690 |  |
| pg_attribution_ready_113 | tag_frequency | sql_feature | sql_feature:secondary:outer_join |  |  | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  |  | 9 | 113 | 0.079646 |  |
| pg_attribution_ready_113 | tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  |  | 14 | 113 | 0.123894 |  |
| pg_attribution_ready_113 | tag_frequency | workload_realism | workload_realism:case_specific:high_join_count |  |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  |  | 23 | 113 | 0.203540 |  |
| pg_attribution_ready_113 | tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity |  |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  |  | 53 | 113 | 0.469027 |  |
| pg_attribution_ready_113 | tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  |  | 12 | 113 | 0.106195 |  |
| pg_attribution_ready_113 | tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  |  | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  |  | 31 | 113 | 0.274336 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | consistency |  | 22 | 113 | 0.194690 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:join | consistency |  | 26 | 113 | 0.230088 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:limit | consistency |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:materialize | consistency |  | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:scan | consistency |  | 29 | 113 | 0.256637 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:set_op | consistency |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:sort | consistency |  | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:subquery | consistency |  | 23 | 113 | 0.203540 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | consistency |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:confirmed:null_semantics_gap | consistency |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:suspected:null_semantics_gap | consistency |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite | consistency |  | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification | consistency |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation | consistency |  | 19 | 113 | 0.168142 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite | consistency |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy | consistency |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown | consistency |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation | consistency |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery | consistency |  | 23 | 113 | 0.203540 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | consistency |  | 9 | 113 | 0.079646 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:set_operation | consistency |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:subquery_in_from | consistency |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from | consistency |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | consistency |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | longtail |  | 24 | 113 | 0.212389 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:join | longtail |  | 24 | 113 | 0.212389 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:limit | longtail |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:materialize | longtail |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:scan | longtail |  | 24 | 113 | 0.212389 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:sort | longtail |  | 24 | 113 | 0.212389 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:subquery | longtail |  | 24 | 113 | 0.212389 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:window | longtail |  | 12 | 113 | 0.106195 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:suspected:datetime_semantics_gap | longtail |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:suspected:null_semantics_gap | longtail |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy | longtail |  | 16 | 113 | 0.141593 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification | longtail |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy | longtail |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite | longtail |  | 20 | 113 | 0.176991 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy | longtail |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:cte | longtail |  | 20 | 113 | 0.176991 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | longtail |  | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:subquery_in_from | longtail |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:window_function | longtail |  | 12 | 113 | 0.106195 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | longtail |  | 12 | 113 | 0.106195 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:secondary:outer_join | longtail |  | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | longtail |  | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count | longtail |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | longtail |  | 16 | 113 | 0.141593 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity | longtail |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism | longtail |  | 12 | 113 | 0.106195 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style | longtail |  | 24 | 113 | 0.212389 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize | performance |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | performance |  | 53 | 113 | 0.469027 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:filter | performance |  | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:join | performance |  | 46 | 113 | 0.407080 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:limit | performance |  | 26 | 113 | 0.230088 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:materialize | performance |  | 14 | 113 | 0.123894 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:scan | performance |  | 53 | 113 | 0.469027 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:set_op | performance |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:sort | performance |  | 39 | 113 | 0.345133 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:window | performance |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | performance |  | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:suspected:datetime_semantics_gap | performance |  | 19 | 113 | 0.168142 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:suspected:type_semantics_gap | performance |  | 11 | 113 | 0.097345 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite | performance |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder | performance |  | 10 | 113 | 0.088496 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy | performance |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown | performance |  | 22 | 113 | 0.194690 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation | performance |  | 10 | 113 | 0.088496 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy | performance |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder | performance |  | 12 | 113 | 0.106195 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy | performance |  | 10 | 113 | 0.088496 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown | performance |  | 24 | 113 | 0.212389 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery | performance |  | 10 | 113 | 0.088496 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:cte | performance |  | 11 | 113 | 0.097345 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:date_time_function | performance |  | 19 | 113 | 0.168142 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | performance |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:set_operation | performance |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:window_function | performance |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | performance |  | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from | performance |  | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | performance |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | performance |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline | performance |  | 53 | 113 | 0.469027 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation | performance |  | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | portability |  | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:filter | portability |  | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:join | portability |  | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:limit | portability |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:scan | portability |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | pool_tag_frequency | plan_operator | plan_operator:present:sort | portability |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:confirmed:datetime_semantics_gap | portability |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:confirmed:identifier_quoting | portability |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:confirmed:limit_fetch_gap | portability |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:confirmed:null_semantics_gap | portability |  | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:confirmed:type_semantics_gap | portability |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | portability | portability:suspected:null_semantics_gap | portability |  | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:dialect_adaptation | portability |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:expression_simplification | portability |  | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:function_normalization | portability |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:order_limit_simplification | portability |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:date_time_function | portability |  | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:primary:expression_complexity | portability |  | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | portability |  | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | portability |  | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity | portability |  | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | pool_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style | portability |  | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | calcite_hep / calcite_hep_fail_closed_120 | 29 | 113 | 0.256637 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:filter |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:join |  | calcite_hep / calcite_hep_fail_closed_120 | 28 | 113 | 0.247788 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:limit |  | calcite_hep / calcite_hep_fail_closed_120 | 10 | 113 | 0.088496 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:materialize |  | calcite_hep / calcite_hep_fail_closed_120 | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:scan |  | calcite_hep / calcite_hep_fail_closed_120 | 31 | 113 | 0.274336 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:set_op |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:sort |  | calcite_hep / calcite_hep_fail_closed_120 | 20 | 113 | 0.176991 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | calcite_hep / calcite_hep_fail_closed_120 | 13 | 113 | 0.115044 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:window |  | calcite_hep / calcite_hep_fail_closed_120 | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:limit_fetch_gap |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:null_semantics_gap |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:datetime_semantics_gap |  | calcite_hep / calcite_hep_fail_closed_120 | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:null_semantics_gap |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:type_semantics_gap |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  | calcite_hep / calcite_hep_fail_closed_120 | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  | calcite_hep / calcite_hep_fail_closed_120 | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  | calcite_hep / calcite_hep_fail_closed_120 | 9 | 113 | 0.079646 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  | calcite_hep / calcite_hep_fail_closed_120 | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  | calcite_hep / calcite_hep_fail_closed_120 | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  | calcite_hep / calcite_hep_fail_closed_120 | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  | calcite_hep / calcite_hep_fail_closed_120 | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  | calcite_hep / calcite_hep_fail_closed_120 | 10 | 113 | 0.088496 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | calcite_hep / calcite_hep_fail_closed_120 | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:date_time_function |  | calcite_hep / calcite_hep_fail_closed_120 | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:outer_join |  | calcite_hep / calcite_hep_fail_closed_120 | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:set_operation |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:subquery_in_from |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:window_function |  | calcite_hep / calcite_hep_fail_closed_120 | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  | calcite_hep / calcite_hep_fail_closed_120 | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:outer_join |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  | calcite_hep / calcite_hep_fail_closed_120 | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity |  | calcite_hep / calcite_hep_fail_closed_120 | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | calcite_hep / calcite_hep_fail_closed_120 | 16 | 113 | 0.141593 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  | calcite_hep / calcite_hep_fail_closed_120 | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  | calcite_hep / calcite_hep_fail_closed_120 | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | calcite_hep / calcite_hep_fail_closed_120 | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | direct_llm / direct_llm_execute_repair_1shot | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:join |  | direct_llm / direct_llm_execute_repair_1shot | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:scan |  | direct_llm / direct_llm_execute_repair_1shot | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:sort |  | direct_llm / direct_llm_execute_repair_1shot | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:outer_join |  | direct_llm / direct_llm_execute_repair_1shot | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | direct_llm / direct_llm_execute_repair_1shot | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | direct_llm / direct_llm_same_engine_rewrite | 27 | 113 | 0.238938 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:filter |  | direct_llm / direct_llm_same_engine_rewrite | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:join |  | direct_llm / direct_llm_same_engine_rewrite | 26 | 113 | 0.230088 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:limit |  | direct_llm / direct_llm_same_engine_rewrite | 12 | 113 | 0.106195 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:materialize |  | direct_llm / direct_llm_same_engine_rewrite | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:scan |  | direct_llm / direct_llm_same_engine_rewrite | 32 | 113 | 0.283186 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:set_op |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:sort |  | direct_llm / direct_llm_same_engine_rewrite | 20 | 113 | 0.176991 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | direct_llm / direct_llm_same_engine_rewrite | 11 | 113 | 0.097345 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:window |  | direct_llm / direct_llm_same_engine_rewrite | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:datetime_semantics_gap |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:identifier_quoting |  | direct_llm / direct_llm_same_engine_rewrite | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:limit_fetch_gap |  | direct_llm / direct_llm_same_engine_rewrite | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:null_semantics_gap |  | direct_llm / direct_llm_same_engine_rewrite | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:type_semantics_gap |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:datetime_semantics_gap |  | direct_llm / direct_llm_same_engine_rewrite | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:null_semantics_gap |  | direct_llm / direct_llm_same_engine_rewrite | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:type_semantics_gap |  | direct_llm / direct_llm_same_engine_rewrite | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite |  | direct_llm / direct_llm_same_engine_rewrite | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  | direct_llm / direct_llm_same_engine_rewrite | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:dialect_adaptation |  | direct_llm / direct_llm_same_engine_rewrite | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  | direct_llm / direct_llm_same_engine_rewrite | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  | direct_llm / direct_llm_same_engine_rewrite | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  | direct_llm / direct_llm_same_engine_rewrite | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  | direct_llm / direct_llm_same_engine_rewrite | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  | direct_llm / direct_llm_same_engine_rewrite | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:expression_simplification |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:function_normalization |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  | direct_llm / direct_llm_same_engine_rewrite | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  | direct_llm / direct_llm_same_engine_rewrite | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:order_limit_simplification |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  | direct_llm / direct_llm_same_engine_rewrite | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  | direct_llm / direct_llm_same_engine_rewrite | 9 | 113 | 0.079646 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | direct_llm / direct_llm_same_engine_rewrite | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:date_time_function |  | direct_llm / direct_llm_same_engine_rewrite | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:expression_complexity |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:outer_join |  | direct_llm / direct_llm_same_engine_rewrite | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:set_operation |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:subquery_in_from |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:window_function |  | direct_llm / direct_llm_same_engine_rewrite | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  | direct_llm / direct_llm_same_engine_rewrite | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:outer_join |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  | direct_llm / direct_llm_same_engine_rewrite | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  | direct_llm / direct_llm_same_engine_rewrite | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity |  | direct_llm / direct_llm_same_engine_rewrite | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | direct_llm / direct_llm_same_engine_rewrite | 15 | 113 | 0.132743 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  | direct_llm / direct_llm_same_engine_rewrite | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | direct_llm / direct_llm_same_engine_rewrite | 9 | 113 | 0.079646 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | sqlglot / sqlglot_optimize_same_dialect | 19 | 113 | 0.168142 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:filter |  | sqlglot / sqlglot_optimize_same_dialect | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:join |  | sqlglot / sqlglot_optimize_same_dialect | 17 | 113 | 0.150442 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:limit |  | sqlglot / sqlglot_optimize_same_dialect | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:materialize |  | sqlglot / sqlglot_optimize_same_dialect | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:scan |  | sqlglot / sqlglot_optimize_same_dialect | 22 | 113 | 0.194690 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:set_op |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:sort |  | sqlglot / sqlglot_optimize_same_dialect | 13 | 113 | 0.115044 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | sqlglot / sqlglot_optimize_same_dialect | 9 | 113 | 0.079646 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:window |  | sqlglot / sqlglot_optimize_same_dialect | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:datetime_semantics_gap |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:identifier_quoting |  | sqlglot / sqlglot_optimize_same_dialect | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:limit_fetch_gap |  | sqlglot / sqlglot_optimize_same_dialect | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:null_semantics_gap |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:type_semantics_gap |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:datetime_semantics_gap |  | sqlglot / sqlglot_optimize_same_dialect | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:null_semantics_gap |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:type_semantics_gap |  | sqlglot / sqlglot_optimize_same_dialect | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite |  | sqlglot / sqlglot_optimize_same_dialect | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  | sqlglot / sqlglot_optimize_same_dialect | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:dialect_adaptation |  | sqlglot / sqlglot_optimize_same_dialect | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  | sqlglot / sqlglot_optimize_same_dialect | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  | sqlglot / sqlglot_optimize_same_dialect | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  | sqlglot / sqlglot_optimize_same_dialect | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:expression_simplification |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:function_normalization |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:order_limit_simplification |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  | sqlglot / sqlglot_optimize_same_dialect | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  | sqlglot / sqlglot_optimize_same_dialect | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | sqlglot / sqlglot_optimize_same_dialect | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:date_time_function |  | sqlglot / sqlglot_optimize_same_dialect | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:expression_complexity |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:outer_join |  | sqlglot / sqlglot_optimize_same_dialect | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:set_operation |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:subquery_in_from |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:window_function |  | sqlglot / sqlglot_optimize_same_dialect | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  | sqlglot / sqlglot_optimize_same_dialect | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:outer_join |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  | sqlglot / sqlglot_optimize_same_dialect | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count |  | sqlglot / sqlglot_optimize_same_dialect | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  | sqlglot / sqlglot_optimize_same_dialect | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | sqlglot / sqlglot_optimize_same_dialect | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  | sqlglot / sqlglot_optimize_same_dialect | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  | sqlglot / sqlglot_optimize_same_dialect | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | sqlglot / sqlglot_optimize_same_dialect | 9 | 113 | 0.079646 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | sqlglot / sqlglot_transpile_same_dialect_noop | 24 | 113 | 0.212389 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:filter |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:join |  | sqlglot / sqlglot_transpile_same_dialect_noop | 25 | 113 | 0.221239 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:limit |  | sqlglot / sqlglot_transpile_same_dialect_noop | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:materialize |  | sqlglot / sqlglot_transpile_same_dialect_noop | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:scan |  | sqlglot / sqlglot_transpile_same_dialect_noop | 26 | 113 | 0.230088 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:set_op |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:sort |  | sqlglot / sqlglot_transpile_same_dialect_noop | 17 | 113 | 0.150442 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | sqlglot / sqlglot_transpile_same_dialect_noop | 13 | 113 | 0.115044 |  |
| pg_attribution_ready_113 | route_tag_frequency | plan_operator | plan_operator:present:window |  | sqlglot / sqlglot_transpile_same_dialect_noop | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:limit_fetch_gap |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:confirmed:null_semantics_gap |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:datetime_semantics_gap |  | sqlglot / sqlglot_transpile_same_dialect_noop | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:null_semantics_gap |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | portability | portability:suspected:type_semantics_gap |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:aggregation_rewrite |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  | sqlglot / sqlglot_transpile_same_dialect_noop | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:materialization_strategy |  | sqlglot / sqlglot_transpile_same_dialect_noop | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:order_limit_simplification |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  | sqlglot / sqlglot_transpile_same_dialect_noop | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  | sqlglot / sqlglot_transpile_same_dialect_noop | 9 | 113 | 0.079646 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  | sqlglot / sqlglot_transpile_same_dialect_noop | 7 | 113 | 0.061947 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  | sqlglot / sqlglot_transpile_same_dialect_noop | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  | sqlglot / sqlglot_transpile_same_dialect_noop | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  | sqlglot / sqlglot_transpile_same_dialect_noop | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  | sqlglot / sqlglot_transpile_same_dialect_noop | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:subquery_decorrelation |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  | sqlglot / sqlglot_transpile_same_dialect_noop | 10 | 113 | 0.088496 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | sqlglot / sqlglot_transpile_same_dialect_noop | 8 | 113 | 0.070796 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:date_time_function |  | sqlglot / sqlglot_transpile_same_dialect_noop | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:outer_join |  | sqlglot / sqlglot_transpile_same_dialect_noop | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:set_operation |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:subquery_in_from |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:primary:window_function |  | sqlglot / sqlglot_transpile_same_dialect_noop | 4 | 113 | 0.035398 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  | sqlglot / sqlglot_transpile_same_dialect_noop | 5 | 113 | 0.044248 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:outer_join |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  | sqlglot / sqlglot_transpile_same_dialect_noop | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  | sqlglot / sqlglot_transpile_same_dialect_noop | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  | sqlglot / sqlglot_transpile_same_dialect_noop | 6 | 113 | 0.053097 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:case_specific:result_size_sensitivity |  | sqlglot / sqlglot_transpile_same_dialect_noop | 1 | 113 | 0.008850 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | sqlglot / sqlglot_transpile_same_dialect_noop | 13 | 113 | 0.115044 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  | sqlglot / sqlglot_transpile_same_dialect_noop | 3 | 113 | 0.026549 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  | sqlglot / sqlglot_transpile_same_dialect_noop | 2 | 113 | 0.017699 |  |
| pg_attribution_ready_113 | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | sqlglot / sqlglot_transpile_same_dialect_noop | 6 | 113 | 0.053097 |  |
| table10_selected_cases | scope_summary_total_rows |  |  |  |  | 7 |  |  | unique_cases=7 |
| table10_selected_cases | scope_summary_tagged_rows |  |  |  |  | 7 | 7 | 1.000000 |  |
| table10_selected_cases | scope_summary_missing_rows |  |  |  |  | 0 | 7 | 0.000000 |  |
| table10_selected_cases | family_frequency | plan_operator |  |  |  | 38 | 7 | 5.428571 |  |
| table10_selected_cases | family_frequency | portability |  |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | family_frequency | rewrite_opportunity |  |  |  | 13 | 7 | 1.857143 |  |
| table10_selected_cases | family_frequency | sql_feature |  |  |  | 14 | 7 | 2.000000 |  |
| table10_selected_cases | family_frequency | workload_realism |  |  |  | 12 | 7 | 1.714286 |  |
| table10_selected_cases | tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | plan_operator | plan_operator:present:aggregate |  |  | 7 | 7 | 1.000000 |  |
| table10_selected_cases | tag_frequency | plan_operator | plan_operator:present:filter |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | plan_operator | plan_operator:present:join |  |  | 7 | 7 | 1.000000 |  |
| table10_selected_cases | tag_frequency | plan_operator | plan_operator:present:limit |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | plan_operator | plan_operator:present:materialize |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | plan_operator | plan_operator:present:scan |  |  | 7 | 7 | 1.000000 |  |
| table10_selected_cases | tag_frequency | plan_operator | plan_operator:present:sort |  |  | 5 | 7 | 0.714286 |  |
| table10_selected_cases | tag_frequency | plan_operator | plan_operator:present:subquery |  |  | 4 | 7 | 0.571429 |  |
| table10_selected_cases | tag_frequency | plan_operator | plan_operator:present:window |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | portability | portability:suspected:datetime_semantics_gap |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | sql_feature | sql_feature:primary:cte |  |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | tag_frequency | sql_feature | sql_feature:primary:date_time_function |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | sql_feature | sql_feature:primary:outer_join |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | sql_feature | sql_feature:primary:window_function |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | sql_feature | sql_feature:secondary:outer_join |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | workload_realism | workload_realism:case_specific:high_join_count |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | consistency |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:join | consistency |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:scan | consistency |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:subquery | consistency |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation | consistency |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery | consistency |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | consistency |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | longtail |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:join | longtail |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:materialize | longtail |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:scan | longtail |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:sort | longtail |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:subquery | longtail |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:window | longtail |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy | longtail |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification | longtail |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite | longtail |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy | longtail |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | sql_feature | sql_feature:primary:cte | longtail |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | sql_feature | sql_feature:primary:outer_join | longtail |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | sql_feature | sql_feature:primary:window_function | longtail |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | pool_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity | longtail |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | pool_tag_frequency | sql_feature | sql_feature:secondary:outer_join | longtail |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density | longtail |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count | longtail |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure | longtail |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism | longtail |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style | longtail |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize | performance |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:aggregate | performance |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:filter | performance |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:join | performance |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:limit | performance |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:materialize | performance |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:scan | performance |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | plan_operator | plan_operator:present:sort | performance |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | pool_tag_frequency | portability | portability:suspected:datetime_semantics_gap | performance |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder | performance |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown | performance |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder | performance |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy | performance |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown | performance |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | sql_feature | sql_feature:primary:date_time_function | performance |  | 2 | 7 | 0.285714 |  |
| table10_selected_cases | pool_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from | performance |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline | performance |  | 3 | 7 | 0.428571 |  |
| table10_selected_cases | pool_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation | performance |  | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:join |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:materialize |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:scan |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:sort |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:window |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:primary:window_function |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:secondary:outer_join |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:case_specific:complex_expression_density |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:case_specific:high_join_count |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | Calcite HEP / calcite_hep_fail_closed_120 | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:join |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:scan |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:sort |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:cte_strategy |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:aggregation_rewrite |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:primary:outer_join |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:secondary:expression_complexity |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:source_inherited:manual_gap_fill_realism |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | Direct LLM + Execute-and-Repair-1 / direct_llm_execute_repair_1shot | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | Direct LLM / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:join |  | Direct LLM / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:limit |  | Direct LLM / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:scan |  | Direct LLM / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:sort |  | Direct LLM / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | portability | portability:suspected:datetime_semantics_gap |  | Direct LLM / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  | Direct LLM / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:materialization_strategy |  | Direct LLM / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:primary:date_time_function |  | Direct LLM / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:secondary:subquery_in_from |  | Direct LLM / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | Direct LLM / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | SQLGlot no-op / same-dialect / sqlglot_transpile_same_dialect_noop | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:join |  | SQLGlot no-op / same-dialect / sqlglot_transpile_same_dialect_noop | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:limit |  | SQLGlot no-op / same-dialect / sqlglot_transpile_same_dialect_noop | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:scan |  | SQLGlot no-op / same-dialect / sqlglot_transpile_same_dialect_noop | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:sort |  | SQLGlot no-op / same-dialect / sqlglot_transpile_same_dialect_noop | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | portability | portability:suspected:datetime_semantics_gap |  | SQLGlot no-op / same-dialect / sqlglot_transpile_same_dialect_noop | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:predicate_pushdown |  | SQLGlot no-op / same-dialect / sqlglot_transpile_same_dialect_noop | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:join_reorder |  | SQLGlot no-op / same-dialect / sqlglot_transpile_same_dialect_noop | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:primary:date_time_function |  | SQLGlot no-op / same-dialect / sqlglot_transpile_same_dialect_noop | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | SQLGlot no-op / same-dialect / sqlglot_transpile_same_dialect_noop | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:delta_relevant:materialize |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 2 | 7 | 0.285714 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:filter |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:join |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 2 | 7 | 0.285714 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:materialize |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:scan |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 2 | 7 | 0.285714 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:sort |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:window |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:expression_simplification |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:join_reorder |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:cte_strategy |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:secondary:predicate_pushdown |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:primary:cte |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:primary:window_function |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:case_specific:long_tail_structure |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:source_inherited:classic_analytical_baseline |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:source_inherited:real_data_correlation |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | workload_realism | workload_realism:source_inherited:realistic_query_style |  | SQLGlot optimize / sqlglot_optimize_same_dialect | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:aggregate |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:join |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:scan |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | plan_operator | plan_operator:present:subquery |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | rewrite_opportunity | rewrite_opportunity:primary:subquery_decorrelation |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:primary:correlated_subquery |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
| table10_selected_cases | route_tag_frequency | sql_feature | sql_feature:primary:outer_join |  | direct_llm / direct_llm_same_engine_rewrite | 1 | 7 | 0.142857 |  |
