# Selected Plan Feature Summary V1

这个文件回答 selected-case plan observability 现在具体保留了哪些证据。
只使用机械选择出来的代表行，不支持 full-denominator observability。
本步骤运行了 plan extraction / EXPLAIN，但没有运行 timing、generation、verifier 或 LLM。
这里给出轻量级 plan feature，不做 full node alignment。

| selected_id | plan_side | plan_format | top_operator | scan_summary | join_summary | aggregate_summary | sort_limit_summary | filter_summary | node_count | parse_confidence | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sel_speedup_01 | source | pg_json | Sort | Seq Scan | Hash Join | Aggregate | Sort | Filter, Hash Cond | 7 | medium | parsed_from_pg_json |
| sel_speedup_01 | rewrite | pg_json | Sort | Seq Scan | Hash Join | Aggregate | Sort | Filter, Hash Cond | 7 | medium | parsed_from_pg_json |
| sel_regression_01 | source | pg_json | Aggregate | Seq Scan | none | Aggregate | none | Filter | 2 | medium | parsed_from_pg_json |
| sel_regression_01 | rewrite | pg_json | Aggregate | Seq Scan | none | Aggregate | none | Filter | 2 | medium | parsed_from_pg_json |
| sel_tie_01 | source | pg_json | Sort | Seq Scan, Subquery Scan | Merge Join, Nested Loop | Aggregate | Sort | Filter, Join Filter, Merge Cond | 31 | medium | parsed_from_pg_json |
| sel_tie_01 | rewrite | pg_json | Sort | Seq Scan, Subquery Scan | Merge Join, Nested Loop | Aggregate | Sort | Filter, Join Filter, Merge Cond | 32 | medium | parsed_from_pg_json |
| sel_failure_01 | source | pg_json | Hash Join | Seq Scan | Hash Join | Aggregate | none | Filter, Hash Cond | 6 | medium | parsed_from_pg_json |
| sel_failure_01 | rewrite | pg_json | Hash Join | Seq Scan | Hash Join | Aggregate | none | Filter, Hash Cond | 6 | medium | parsed_from_pg_json |
| sel_sqlglot_extra_01 | source | spark_text | HashAggregate | Scan | none_visible | Aggregate, HashAggregate | none_visible | Filter, Condition | 12 | low | parsed_from_spark_formatted_text |
| sel_sqlglot_extra_01 | rewrite | spark_text | HashAggregate | Scan | none_visible | Aggregate, HashAggregate | none_visible | Filter, Condition | 12 | low | parsed_from_spark_formatted_text |

这些 feature 只支持 selected-case 级别的可观察性描述，不支持全量归因。
