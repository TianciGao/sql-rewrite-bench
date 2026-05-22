This is paper-facing synthesis from retained artifacts. It does not create a final ranked leaderboard. Gaps below mark where retained evidence stops and new governed work would begin.

| `gap_id` | `affected_table` | `gap_type` | `current_status` | `required_next_artifact_or_experiment` | `priority` | `can_be_done_by_aggregation_only` | `requires_new_execution` | `paper_risk_if_not_done` | `notes` |
|---|---|---|---|---|---|---|---|---|---|
| `gap_01` | `Table 4` | `method_level_negative_rejection_non_control_rows` | `NA_not_computed` | `method_specific_hard_negative_guardrail_aggregation_or_new_guardrail_run` | `high` | `no` | `yes` | `medium` | `Control-route hard-negative evidence exists but method-level negative rejection does not.` |
| `gap_02` | `Table 7` | `run_event_long_failure_export` | `missing` | `case_level_run_event_long_or_failure_event_export` | `high` | `no` | `yes` | `medium` | `Needed to name concrete failure exemplars rather than route-level summaries only.` |
| `gap_03` | `Table 6` | `sqlglot_full_per_case_timing_export` | `aggregate_only_no_case_rows` | `retained_full_sqlglot_per_case_timing_rows` | `high` | `no` | `yes` | `medium` | `SQLGlot timing summaries exist but per-case rows are incomplete.` |
| `gap_04` | `Table 8` | `port_denominator_completion` | `bounded_port6_only` | `explicit_port9_packet_or_explicitly_frozen_selected_port_subset` | `high` | `no` | `yes` | `high` | `Current Track C is bounded PORT6 only.` |
| `gap_05` | `Table 8` | `SpeedupTransferRate` | `NA_not_computed` | `target_engine_exact_timed_transfer_packet` | `medium` | `no` | `yes` | `medium` | `No retained target-engine exact timed transfer evidence.` |
| `gap_06` | `Table 9` | `CONS9_verifier_support` | `canary_or_smoke_only` | `verifier_compatible_cons9_or_selected_pair_matrix` | `high` | `no` | `yes` | `medium` | `Current verifier support is SQLSolver smoke and VeriEQL canary only.` |
| `gap_07` | `Table 10` | `method_specific_plan_extraction` | `selected_case_only_needs_plan_extraction` | `retained_method_specific_source_and_rewrite_plan_exports_for_selected_cases` | `high` | `no` | `yes` | `medium` | `Selected cases are known but method-specific plans are not retained.` |
| `gap_08` | `Table 10` | `node_alignment` | `needs_node_alignment` | `node_alignment_output_for_selected_case_set` | `high` | `no` | `yes` | `medium` | `No selected case has retained node alignment evidence.` |
| `gap_09` | `Table 10` | `attribution` | `attribution_not_supported_by_retained_artifacts` | `attribution_mapping_or_operator_level_link` | `medium` | `no` | `yes` | `low` | `Attribution cannot be claimed without new retained artifacts.` |
| `gap_10` | `Table 10` | `case_level_failure_exemplar` | `needs_case_level_failure_row` | `case_level_failure_event_export` | `medium` | `no` | `yes` | `low` | `Failure row currently uses placeholder selected_case_id.` |
| `gap_11` | `Table 3_or_future_appendix` | `direct_llm_execute_and_repair_future_expansion` | `not_started` | `governed_new_route_packet_if_future_expansion_is_desired` | `low` | `no` | `yes` | `low` | `Only relevant if a future paper revision wants broader baseline expansion.` |

**Interpretation notes**

- These are paper-facing gap statements, not permissions to run new experiments automatically.
- `requires_new_execution=yes` means the current freeze folder cannot close the gap by aggregation alone.
