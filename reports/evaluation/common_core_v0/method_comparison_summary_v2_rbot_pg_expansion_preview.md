# Method Comparison Summary v2 R-Bot PG Expansion Preview

This is a preview only. It is **not** the canonical comparison table.

This preview shows what `method_comparison_summary_v2` would look like if the
current R-Bot PG7 row were replaced by the newer denominator-aware PostgreSQL
expansion v2 evidence.

Warning:

- this preview is still **not** a single scalar leaderboard
- rows use different route structures, engine scopes, and timing denominators
- `leaderboard_comparable = no` means a row is useful evidence but not directly
  rank-comparable without explicit denominator normalization

| method_id | route_id | method_family | evidence_type | generation_or_route_denominator_id | execution_or_ready_denominator_id | timing_denominator_id | engine_scope | planned_generation_or_route_rows | generated_or_ready_rows | executed_rows | match_exact_rows | timing_success_rows | executable_rate | result_consistency_rate | gm_speedup | regression_rate_20pct | leaderboard_comparable |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `sqlglot` | `sqlglot_combined_same_engine` | `sqlglot` | `aggregate_route_summary` | `sqlglot_combined_same_engine_240` | `attempted_153` | `timing_success_137_on_common_core_v0_40_combined` | `tri_engine_same_engine` | `240` | `153` | `137` | `137` | `137` | `0.5708` | `0.5708` | `1.0179` | `0.0511` | `no` |
| `sqlglot` | `sqlglot_optimize_same_dialect` | `sqlglot` | `route_summary` | `common_core_v0_40_same_engine_120_optimize_route` | `attempted_75` | `timing_success_65_on_optimize_route` | `tri_engine_same_engine` | `120` | `75` | `65` | `65` | `65` | `0.5417` | `0.5417` | `1.0168` | `0.0615` | `no` |
| `sqlglot` | `sqlglot_transpile_same_dialect_noop` | `sqlglot` | `route_summary` | `common_core_v0_40_same_engine_120_transpile_noop_route` | `attempted_78` | `timing_success_72_on_transpile_noop_route` | `tri_engine_same_engine` | `120` | `78` | `72` | `72` | `72` | `0.6000` | `0.6000` | `1.0190` | `0.0417` | `no` |
| `direct_llm` | `direct_llm_same_engine_rewrite` | `direct_llm` | `route_summary` | `common_core_v0_40` | `ready_to_execute_115` | `timing_success_94_on_common_core_v0_40` | `tri_engine_same_engine` | `120` | `115` | `99` | `94` | `94` | `0.8250` | `0.7833` | `1.0436` | `0.0319` | `no` |
| `calcite_hep` | `calcite_hep_pg_rewrite` | `calcite_hep` | `pg_only_route_summary` | `common_core_v0_40_pg40` | `ready_to_execute_29` | `timing_success_21_on_common_core_v0_40_pg40` | `pg_only` | `40` | `29` | `23` | `21` | `21` | `0.5750` | `0.5250` | `1.0267` | `0.2381` | `no` |
| `r_bot` | `r_bot_same_engine_rewrite` | `r_bot` | `pg_expansion_v2_route_summary` | `common_core_v0_40_pg40` | `generated_pg15_from_pg40_expansion_only` | `generated_pg15_from_pg40_expansion_match_exact_only` | `pg_only` | `40` | `15` | `15` | `15` | `15` | `0.3750` | `0.3750` | `0.921825` | `0.2000` | `no` |

## R-Bot Caveat

R-Bot PG expansion v2 improves PostgreSQL generation coverage from PG7 to PG15
match-exact timing evidence, but remains PG-only and subset-scoped. It is not
full PG40 timing, not full 120 same-engine timing, not tri-engine evidence, and
not leaderboard-comparable.
