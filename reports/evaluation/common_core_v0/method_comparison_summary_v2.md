**Method Comparison Summary v2**

This is a denominator-aware comparison ledger for `common_core_v0`.

Warning:
- this file is **not** a single scalar leaderboard
- rows use different route structures, engine scopes, and timing denominators
- `leaderboard_comparable = no` means the row is useful evidence but not directly rank-comparable without explicit denominator normalization

The CSV artifact is the canonical full-schema table. The compact markdown table below highlights the paper-facing fields most likely to be compared incorrectly if denominator labels are ignored.

| method_id | route_id | method_family | evidence_type | generation_or_route_denominator_id | execution_or_ready_denominator_id | timing_denominator_id | engine_scope | planned_generation_or_route_rows | generated_or_ready_rows | executed_rows | match_exact_rows | timing_success_rows | executable_rate | result_consistency_rate | gm_speedup | regression_rate_20pct | leaderboard_comparable |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `sqlglot` | `sqlglot_combined_same_engine` | `sqlglot` | `aggregate_route_summary` | `sqlglot_combined_same_engine_240` | `attempted_153` | `timing_success_137_on_common_core_v0_40_combined` | `tri_engine_same_engine` | `240` | `153` | `137` | `137` | `137` | `0.5708` | `0.5708` | `1.0179` | `0.0511` | `no` |
| `sqlglot` | `sqlglot_optimize_same_dialect` | `sqlglot` | `route_summary` | `common_core_v0_40_same_engine_120_optimize_route` | `attempted_75` | `timing_success_65_on_optimize_route` | `tri_engine_same_engine` | `120` | `75` | `65` | `65` | `65` | `0.5417` | `0.5417` | `1.0168` | `0.0615` | `no` |
| `sqlglot` | `sqlglot_transpile_same_dialect_noop` | `sqlglot` | `route_summary` | `common_core_v0_40_same_engine_120_transpile_noop_route` | `attempted_78` | `timing_success_72_on_transpile_noop_route` | `tri_engine_same_engine` | `120` | `78` | `72` | `72` | `72` | `0.6000` | `0.6000` | `1.0190` | `0.0417` | `no` |
| `direct_llm` | `direct_llm_same_engine_rewrite` | `direct_llm` | `route_summary` | `common_core_v0_40` | `ready_to_execute_115` | `timing_success_94_on_common_core_v0_40` | `tri_engine_same_engine` | `120` | `115` | `99` | `94` | `94` | `0.8250` | `0.7833` | `1.0436` | `0.0319` | `no` |
| `calcite_hep` | `calcite_hep_pg_rewrite` | `calcite_hep` | `pg_only_route_summary` | `common_core_v0_40_pg40` | `ready_to_execute_29` | `timing_success_21_on_common_core_v0_40_pg40` | `pg_only` | `40` | `29` | `23` | `21` | `21` | `0.5750` | `0.5250` | `1.0267` | `0.2381` | `no` |
| `r_bot` | `r_bot_same_engine_rewrite` | `r_bot` | `pg_expansion_v2_route_summary` | `common_core_v0_40_pg40` | `generated_pg15_from_pg40_expansion_only` | `generated_pg15_from_pg40_expansion_match_exact_only` | `pg_only` | `40` | `15` | `15` | `15` | `15` | `0.3750` | `0.3750` | `0.921825` | `0.2000` | `no` |

## Notes

- `executable_rate` and `result_consistency_rate` are planned-denominator rates in this table.
- `negative_rejection_rate` is retained in the CSV schema but currently `NA_not_computed` for all rows because a common normalized rejection definition has not yet been frozen across these method families.
- `cross_engine_executable_rate`, `cross_engine_consistency_rate`, and `speedup_transfer_rate` are carried as `NA_not_computed` because aligned cross-engine benefit evidence is not yet available.
- Support and diagnostic fields are retained in schema for future integration but are not used as ranking columns here.

## Why R-Bot Is Included But Not Leaderboard-Comparable

R-Bot has denominator-aware formal evidence and should be visible in the comparison ledger, but:

- its current comparison row is based on the PostgreSQL expansion path, not a tri-engine same-engine packet
- its generation denominator is `common_core_v0_40_pg40`
- its valid execution subset is `generated_pg15_from_pg40_expansion_only`
- its timing subset is `generated_pg15_from_pg40_expansion_match_exact_only`
- its retained timing evidence is still PostgreSQL-only and subset-scoped
- the earlier PG7 evidence remains retained historically, but the table now shows the newer PG expansion v2 row as the latest R-Bot evidence

Therefore it is useful evidence, but not directly comparable to full-denominator same-engine timing rows without explicit denominator normalization.
