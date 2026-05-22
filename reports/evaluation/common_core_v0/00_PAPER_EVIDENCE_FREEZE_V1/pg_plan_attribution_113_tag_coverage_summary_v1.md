# PG Plan Attribution 113 Tag Coverage Summary V1

This file summarizes tag coverage after executing the 113-row PG frontier.
中文说明：tag coverage 只是 PG frontier 的 retained scope，不是 full common-core attribution completion。

| summary_scope | summary_name | planned_candidates | both_plan_success | tagged_candidates | tag_count | tag_families_present | missing_tags_after_execution | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | pg_plan_attribution_113 | 113 | 113 | 113 | 56 | plan_operator\|portability\|rewrite_opportunity\|sql_feature\|workload_realism | none_within_executed_frontier | overall frontier tag coverage summary |
| pool | consistency | 29 | 29 | 29 | 24 | plan_operator\|portability\|rewrite_opportunity\|sql_feature\|workload_realism | none_within_pool_frontier |  |
| pool | longtail | 24 | 24 | 24 | 27 | plan_operator\|portability\|rewrite_opportunity\|sql_feature\|workload_realism | none_within_pool_frontier |  |
| pool | performance | 53 | 53 | 53 | 34 | plan_operator\|portability\|rewrite_opportunity\|sql_feature\|workload_realism | none_within_pool_frontier |  |
| pool | portability | 7 | 7 | 7 | 22 | plan_operator\|portability\|rewrite_opportunity\|sql_feature\|workload_realism | none_within_pool_frontier |  |
