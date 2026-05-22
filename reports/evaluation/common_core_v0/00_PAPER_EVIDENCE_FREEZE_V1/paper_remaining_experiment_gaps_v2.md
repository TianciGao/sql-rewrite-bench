# Paper Remaining Experiment Gaps v2

这是刷新后的 remaining gaps 清单。
重点是区分：哪些已经 resolved / lowered，哪些仍然需要新执行或新工件。

| gap_id | affected_table | gap_type | current_status | required_next_artifact_or_experiment | priority | can_be_done_by_aggregation_only | requires_new_execution | paper_risk_if_not_done | notes |
|---|---|---|---|---|---|---|---|---|---|
| gap_01 | Table 4 | method_level_negative_rejection_non_control_rows | NA_not_computed | method_specific_hard_negative_guardrail_aggregation_or_new_guardrail_run | high | no | yes | medium | Control-route hard-negative evidence exists but method-level negative rejection still does not. |
| gap_02 | Table 7 | case_level_failure_export | resolved_by_case_level_failure_export | none_for_current_table_refresh | resolved | yes | no | low | 198 case-level failure rows are now exported and Table 7 v2 uses them. |
| gap_03 | Table 10 | case_level_failure_exemplar | resolved_by_case_level_failure_export | none_for_case_identity | resolved | yes | no | low | Table 10 v2 now uses CONS_0024 / pg / direct_llm / mismatch. |
| gap_04 | Table 6 | sqlglot_full_per_case_timing_export | aggregate_only_no_case_rows | retained_full_sqlglot_per_case_timing_rows | high | no | yes | medium | SQLGlot timing summaries exist but route-level full per-case rows are still incomplete. |
| gap_05 | Table 3_and_Table_6 | calcite_hep_full120_timing | lowered_after_exact93_timing_packet | only_needed_if_future_work_demands_full120_timing_packet | medium | no | yes | low | The 93 exact-row timing gap is resolved for current paper-safe use, but this is not full 120 timing. |
| gap_06 | Future_repair_route_expansion | direct_llm_execute_repair_route | resolved_for_1shot_route | new_governed_route_packet_only_if_future_expansion_is_desired | resolved | no | yes | low | Direct LLM execute-and-repair 1-shot route now exists; broader repair policies remain optional future work. |
| gap_07 | Table 8 | port_denominator_completion | bounded_port6_only | explicit_port9_packet_or_explicitly_frozen_selected_port_subset | high | no | yes | high | Current Track C remains bounded PORT6 only. |
| gap_08 | Table 8 | SpeedupTransferRate | NA_not_computed | target_engine_exact_timed_transfer_packet | medium | no | yes | medium | No retained target-engine exact timed transfer evidence. |
| gap_09 | Table 9 | CONS9_verifier_support | canary_or_smoke_only | verifier_compatible_cons9_or_selected_pair_matrix | high | no | yes | medium | Current verifier support is SQLSolver smoke and VeriEQL canary only. |
| gap_10 | Table 10 | method_specific_plan_extraction | selected_case_only_needs_plan_extraction | retained_method_specific_source_and_rewrite_plan_exports_for_selected_cases | high | no | yes | medium | Selected cases are known but method-specific plans are still not retained. |
| gap_11 | Table 10 | node_alignment_and_attribution | needs_node_alignment_and_attribution | node_alignment_output_and_attribution_mapping_for_selected_cases | high | no | yes | medium | Table 10 v2 still cannot claim node alignment or plan attribution. |
| gap_12 | Appendix_methods | r_bot_and_learnedrewrite_full_failure_frontier | summary_only_or_bounded | full_row_level_failure_frontier_if_future_appendix_deepening_is_desired | low | no | yes | low | R-Bot and LearnedRewrite remain appendix-only and do not block current main-paper claims. |

## Interpretation Notes

- 已经解决或显著降低的缺口：Direct LLM repair 1-shot route、Calcite 93 exact-row timing、case-level failure export、Table 10 failure exemplar。
- 仍然显著存在的缺口：SQLGlot full per-case timing、node alignment、attribution、PORT9、SpeedupTransferRate、CONS9 verifier support。
