# Common-core v0 Taxonomy Coverage v1

## Purpose

这个文件回答什么问题：把 Common-core v0 的 4+1 retained case tag evidence 聚合成可用于 Section 8.3 和 Appendix B 的 taxonomy coverage summary。

## Denominator

- Common-core v0 fixed denominator: `40` cases
- Pool split: `PERF=16`, `CONS=9`, `PORT=9`, `LONGTAIL=6`
- Tag evidence source: retained case-level normalized tags only

## Coverage summary table

| axis | distinct_tags_covered | cases_with_at_least_one_tag | case_denominator | top_tags | primary_tag_count | secondary_tag_count | confirmed_portability_tag_count | suspected_portability_tag_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sql_feature | 11 | 32 | 40 | sql_feature:primary:date_time_function:11|sql_feature:primary:correlated_subquery:10|sql_feature:primary:cte:8|sql_feature:primary:outer_join:6|sql_feature:secondary:expression_complexity:6 | 8 | 3 | NA_not_applicable | NA_not_applicable |
| rewrite_opportunity | 18 | 40 | 40 | rewrite_opportunity:primary:dialect_adaptation:9|rewrite_opportunity:primary:subquery_decorrelation:9|rewrite_opportunity:secondary:predicate_pushdown:8|rewrite_opportunity:primary:predicate_pushdown:7|rewrite_opportunity:secondary:aggregation_rewrite:7 | 9 | 9 | NA_not_applicable | NA_not_applicable |
| plan_operator | 11 | 40 | 40 | plan_operator:present:scan:40|plan_operator:present:aggregate:34|plan_operator:present:join:32|plan_operator:present:sort:23|plan_operator:present:limit:13 | 0 | 0 | NA_not_applicable | NA_not_applicable |
| workload_realism | 8 | 32 | 40 | workload_realism:source_inherited:classic_analytical_baseline:16|workload_realism:source_inherited:realistic_query_style:15|workload_realism:case_specific:complex_expression_density:7|workload_realism:case_specific:long_tail_structure:6|workload_realism:case_specific:result_size_sensitivity:4 | 0 | 0 | NA_not_applicable | NA_not_applicable |
| portability | 9 | 24 | 40 | portability:confirmed:identifier_quoting:9|portability:suspected:datetime_semantics_gap:7|portability:confirmed:limit_fetch_gap:6|portability:confirmed:type_semantics_gap:6|portability:confirmed:datetime_semantics_gap:5 | 0 | 0 | 6 | 3 |

## How to read the tags

- Canonical unit: retained `normalized_tags` strings.
- `primary` / `secondary` are detected from the namespace component in retained tags, for example `sql_feature:primary:*` and `rewrite_opportunity:secondary:*`.
- `confirmed` / `suspected` portability are detected from `portability:confirmed:*` and `portability:suspected:*`.
- Empty namespace cells in the case matrix mean no retained tag in that namespace for that case; they are not inferred from prose or source family.

## What this supports

- A paper-facing characterization of the controlled Common-core v0 coverage surface.
- Pool-aware discussion of different stress types: performance, consistency, portability, and longtail realism/structure.
- Appendix B style per-case tag matrix based on retained evidence only.

## What this does not support

- This is not method ranking.
- This is not workload-frequency estimation.
- This does not prove taxonomy completeness outside the frozen Common-core v0 denominator.
- This does not infer tags from source_family, pool name, or method behavior.

## Safe prose snippet for the paper

Common-core v0 exposes a controlled taxonomy coverage surface across five retained tag axes: SQL features, rewrite opportunities, plan/operator families, workload realism, and portability risks. These counts are benchmark-characterization metadata rather than method rankings or workload-frequency estimates. The 40-case denominator is intentionally curated, and different pools contribute different stress types rather than forming a representative sample of production query frequencies.
