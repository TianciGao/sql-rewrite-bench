# Table 10 Failure Exemplar Selection v1

这是基于已保留工件的 paper-facing 综合导出。

- 未进行任何新的执行。
- 未运行数据库、checker、timing、LLM 或 verifier。
- 这不是最终排行榜。

| selected | case_id | pool | engine | method_id | route_id | failure_category | failure_detail | reason_selected | source_artifacts | table10_update_recommendation | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| true | CONS_0024 | consistency | pg | direct_llm | direct_llm_same_engine_rewrite | mismatch | exact_match=false; sorted_match=false | clear Direct LLM mismatch row with concrete result_check artifact on the main same-engine route | reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/workspaces/CONS_0024/pg/direct_llm_same_engine_rewrite/result_check.json|reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/logs/cons_0024__pg__direct_llm_same_engine_rewrite.stderr.log | replace needs_case_level_failure_row with this concrete mismatch exemplar; keep plan fields unresolved unless method-specific plans are later retained | preferred selection order item 1 satisfied |
| false | LONGTAIL_0023 | longtail | pg | direct_llm | direct_llm_same_engine_rewrite | execution_failed | Command '['psql', '-v', 'ON_ERROR_STOP=1', '-X', '-q', '-c', 'SET search_path TO ccv0_direct_llm_longtail_0023_pg;', '-c', "COPY (WITH OutboundLinks AS (\n    SELECT\n        pl.PostId,\n        COUNT(*) AS outbound_count\n    FROM\n        PostLinks pl\n    GROUP BY\n        pl.PostId\n),\nInboundLinks AS (\n    SELECT\n        pl.RelatedPostId AS PostId,\n        COUNT(*) AS inbound_count\n    FROM\n        PostLinks pl\n    GROUP BY\n        pl.RelatedPostId\n)\nSELECT\n    p.Id AS PostId,\n    p.Title,\n    COALESCE(o.outbound_count, 0) AS outbound_count,\n    COALESCE(i.inbound_count, 0) AS inbound_count,\n    COALESCE(o.outbound_count, 0) + COALESCE(i.inbound_count, 0) AS total_links\nFROM\n    Posts p\nLEFT JOIN\n    OutboundLinks o ON o.PostId = p.Id\nLEFT JOIN\n    InboundLinks i ON i.PostId = p.Id\nWHERE\n    total_links > 0\nORDER BY\n    total_links DESC,\n    p.Id) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"]' returned non-zero exit status 1. | backup_direct_llm_execution_failed | reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/workspaces/LONGTAIL_0023/pg/direct_llm_same_engine_rewrite/result_check.json|reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01/logs/longtail_0023__pg__direct_llm_same_engine_rewrite.stderr.log | keep as fallback only | backup candidate |
| false | CONS_0024 | consistency | mysql | direct_llm | direct_llm_execute_repair_1shot | execution_failed | not_checked_execution_failed | backup_repair_remaining_failure | reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/workspaces/CONS_0024/mysql/direct_llm_execute_repair_1shot/result_check.json|reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/logs/direct_llm_repair_001.execution.stderr.log | keep as fallback only | backup candidate |

## Interpretation Notes

- 优先选择 Direct LLM 主路由中的 concrete mismatch 行。
- 当前已可替换掉旧的 needs_case_level_failure_row 占位。
- 这仍然只支持 failure exemplar，不支持计划归因。
