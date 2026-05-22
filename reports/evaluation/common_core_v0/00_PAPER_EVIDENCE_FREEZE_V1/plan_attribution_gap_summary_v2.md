# Plan Attribution Gap Summary V2

This gap summary records what the reviewed 24-row PG attribution packet resolved and what remains out of scope.
中文说明：24 行 packet 已经增强 selected-case 归因，但 full-denominator attribution 仍然没有解决。

| gap_id | affected_table | current_status | gap_description | resolved_by_this_packet | remaining_gap | requires_new_execution | priority | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| plan_attr_gap_01 | Table 5 v4 | selected_pg_packet_added | Main routes now have reviewed PG node-delta coverage on 24 exact-timed rows, but denominator-wide plan coverage is still unavailable. | selected_pg_attribution_rows_for_5_main_routes | no_full_denominator_plan_coverage | yes | medium | Future expansion would need a larger reviewed PG plan packet or separate engine-specific packets. |
| plan_attr_gap_02 | Table 10 v4 | selected_case_node_delta_strengthened | Route-level plan deltas are now retained for 24 exact-timed PG rows. | node_level_pg_explain_analyze_buffers_artifacts | failure_diagnostic_row_still_separate | yes | medium | Failure observability should remain in the separate failure-side Table 10 lineage. |
| plan_attr_gap_03 | Table 10 v4 | still_selected_case_only | Heuristic node alignment and attribution confidence are packet-local only. | partial_only | no_global_node_alignment_or_causal_attribution | yes | high | Do not overclaim beyond medium/low confidence for selected rows. |
