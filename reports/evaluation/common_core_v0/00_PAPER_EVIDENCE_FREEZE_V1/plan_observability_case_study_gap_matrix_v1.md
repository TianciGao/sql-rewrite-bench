This is paper-facing synthesis from retained artifacts. It does not create a final ranked leaderboard. Table 10 is a selected case study, not full-denominator plan attribution.

| `gap_id` | `table10_field` | `affected_outcome_type` | `affected_method_route` | `current_status` | `required_next_artifact` | `requires_new_experiment` | `notes` |
|---|---|---|---|---|---|---|---|
| `table10_gap_source_plan_01` | `source_plan_pattern` | `speedup` | `direct_llm/direct_llm_same_engine_rewrite` | `needs_new_plan_extraction` | `retained_method_specific_source_plan_export` | `yes` | `controls-side source plans exist for some cases but do not establish method-row observability` |
| `table10_gap_rewrite_plan_01` | `rewrite_plan_pattern` | `speedup` | `direct_llm/direct_llm_same_engine_rewrite` | `needs_new_plan_extraction` | `retained_method_specific_rewrite_plan_export` | `yes` | `no retained method-specific rewrite plan file for selected direct_llm case` |
| `table10_gap_delta_01` | `main_plan_delta` | `regression` | `direct_llm/direct_llm_same_engine_rewrite` | `needs_node_alignment` | `node_alignment_or_delta_summary` | `yes` | `without aligned source/rewrite plans no causal delta can be stated` |
| `table10_gap_attr_01` | `attribution_confidence` | `tie_or_near_neutral` | `r_bot/r_bot_same_engine_rewrite` | `attribution_not_supported_by_retained_artifacts` | `attribution_mapping_or_operator_level_link` | `yes` | `retained timing row exists but no attribution artifact` |
| `table10_gap_failure_01` | `case-level failure artifact` | `failure` | `direct_llm/direct_llm_same_engine_rewrite` | `needs_case_level_failure_row` | `run_event_long_or_failure_event_export` | `yes` | `Table 7 retains only route-level failure accounting not a concrete case row` |
| `table10_gap_alignment_01` | `node alignment` | `all` | `selected_table10_rows` | `needs_node_alignment` | `node_alignment_output_for_selected_case_set` | `yes` | `no selected case has retained node alignment evidence` |
| `table10_gap_norm_01` | `plan normalization` | `all` | `selected_table10_rows` | `needs_new_plan_extraction` | `normalized_source_and_rewrite_plan_views` | `yes` | `selected case study cannot compare heterogeneous raw plan formats without a normalization step` |

**Interpretation notes**

- The gap matrix is intentionally explicit about what is missing before a richer case-study narrative can be claimed.
- Missing plan extraction, node alignment, and attribution are support-track gaps, not correctness or timing failures.
