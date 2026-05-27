# Plan Observability Case Study Gap Matrix V3

这个文件回答：selected-case observability packet 解决了哪些 gap，还剩哪些 gap。
它只更新 observability gap，不改变 correctness / timing 结论。

| gap_id | affected_table | current_status | gap_description | resolved_by_this_packet | remaining_gap | requires_new_execution | priority | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| obs_gap_01 | Table 5 | selected_case_observability_packet_retained | selected representative source/rewrite plan pairs are now retained | yes | not full denominator plan extraction | yes | medium | This packet improves observability evidence but does not create denominator-wide coverage metrics. |
| obs_gap_02 | Table 10 | selected_case_plan_fields_backfilled | speedup/regression/tie/failure rows now have retained plan artifacts and bounded delta classes | yes | no full node alignment | yes | high | Failure exemplar identity was already resolved; this packet resolves the missing selected-case plan pair layer. |
| obs_gap_03 | Table 10 | selected_case_only | operator-level attribution remains bounded and low/medium confidence only | partial | causal attribution not denominator-wide and not node-aligned | yes | high | Do not turn lightweight plan-feature deltas into global causal claims. |
| obs_gap_04 | RQ2_overall | selected_case_support_available | selected-case observability is now stronger than raw latency labels alone | partial | no full PlanParseRate or NodeAlignmentCoverage metric | yes | medium | This packet supports qualitative observability evidence only. |

仍然不能说 full-denominator node alignment、AttributionCoverage 或 global causal attribution。
