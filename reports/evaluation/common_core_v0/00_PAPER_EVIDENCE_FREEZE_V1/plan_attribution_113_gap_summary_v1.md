# Plan Attribution 113 Gap Summary V1

This file records what the 113-row PG frontier resolves and what still remains out of scope.
中文说明：113 行 PG frontier 虽然大幅扩展了 tag-aware observability，但仍然不是 full-denominator 或 global causal attribution。

| gap_id | scope_name | current_status | remaining_gap | requires_new_execution | priority | notes |
| --- | --- | --- | --- | --- | --- | --- |
| attr113_gap_01 | pg_only_frontier_scope | resolved_for_pg_ready_113_frontier_only | not_full_120_and_not_cross_engine | yes | medium | This packet is PG-only and frontier-based, not denominator-wide or cross-engine attribution. |
| attr113_gap_02 | global_causal_attribution | still_unresolved | no_denominator_wide_causal_attribution | yes | high | Even with 113 rows, attribution remains PG-only and selected-frontier evidence. |
| attr113_gap_03 | remaining_tag_absence | still_visible_after_113 | portability:confirmed:boolean_semantics_gap | yes | medium | The boolean_semantics_gap slice remains absent after the 113-row PG-ready frontier. |
