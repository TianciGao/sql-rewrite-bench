**Method Comparison Summary**
This is a coverage-aware same-engine method comparison summary for `common_core_v0_40`, now including denominator-labeled R-Bot evidence.

It should be treated as a **pre-leaderboard comparison**, not a final leaderboard.

Why this is not a final leaderboard:
- SQLGlot same-engine evidence spans **two explicit routes**: `sqlglot_optimize_same_dialect` and `sqlglot_transpile_same_dialect_noop`.
- Direct LLM same-engine evidence spans **one route**: `direct_llm_same_engine_rewrite`.
- R-Bot same-engine evidence spans **one route**: `r_bot_same_engine_rewrite`, but only `7` PostgreSQL rows reached valid timing from the formal `120`-row generation denominator.
- SQLGlot therefore has a `240`-row planned same-engine route denominator, while Direct LLM and R-Bot each start from a `120`-row planned generation denominator.
- Benchmark support / controls readiness, verifier-support, and plan-observability metrics remain separate from method ranking metrics.
- R-Bot timing is a **PG7 subset denominator**, not a full-denominator timing packet, so explicit denominator labels are required.

Coverage-aware key comparison:

| method_group | route_id | generation_or_route_denominator | execution_or_ready_denominator | timing_denominator | planned_rows | attempted_or_ready_rows | executable_rate_planned | executable_rate_attempted_or_ready | result_consistency_rate_planned | result_consistency_rate_executed | timing_success_rows | coverage_planned | coverage_timing_eligible | GM_Speedup | RegressionRate@20% | leaderboard_comparable_without_denominator_labels |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `sqlglot` | `sqlglot_combined_same_engine` | `240 combined same-engine route rows` | `attempted = 153` | `137 timing-success rows on common_core_v0_40 combined same-engine aggregate` | `240` | `153` | `0.5708` | `0.8954` | `0.5708` | `0.8954` | `137` | `0.5708` | `1.0000` | `1.0179` | `0.0511` | `no` |
| `sqlglot` | `sqlglot_optimize_same_dialect` | `120 route rows` | `attempted = 75` | `65 timing-success rows on 120-row optimize route slice` | `120` | `75` | `0.5417` | `0.8667` | `0.5417` | `0.8667` | `65` | `0.5417` | `1.0000` | `1.0168` | `0.0615` | `no` |
| `sqlglot` | `sqlglot_transpile_same_dialect_noop` | `120 route rows` | `attempted = 78` | `72 timing-success rows on 120-row transpile/noop route slice` | `120` | `78` | `0.6000` | `0.9231` | `0.6000` | `0.9231` | `72` | `0.6000` | `1.0000` | `1.0190` | `0.0417` | `no` |
| `direct_llm` | `direct_llm_same_engine_rewrite` | `120 planned same-engine rows` | `ready_to_execute = 115` | `94 timing-success rows on common_core_v0_40` | `120` | `115` | `0.8250` | `0.8609` | `0.7833` | `0.9495` | `94` | `0.7833` | `1.0000` | `1.0436` | `0.0319` | `no` |
| `r_bot` | `r_bot_same_engine_rewrite` | `120 planned same-engine rows` | `generated_pg7_only = 7` | `generated_pg7_match_exact_only = 7` | `120` | `7` | `0.0583` | `1.0000` | `0.0583` | `1.0000` | `7` | `0.0583` | `1.0000` | `0.947444` | `0.2857` | `no` |

## Interpretation

### Denominator differences

- SQLGlot combined same-engine reporting should not be read as “one route versus one route”. It is the aggregate of two distinct same-engine routes with different generation and skip behavior.
- Direct LLM is a single-route same-engine packet, so its `120` planned rows are structurally different from SQLGlot’s `240` combined rows.
- R-Bot is also a single-route packet, but its valid timing evidence is only the `generated_pg7_match_exact_only` subset rather than a full-denominator timing run.
- A route-to-route comparison is more defensible than a flattened method-family ranking.
- Any table row containing R-Bot must carry explicit generation, execution, and timing denominator labels.

### Validity and execution

- Direct LLM has the strongest single-route validity coverage in the current evidence: `executable_rate_over_planned = 0.8250` and `result_consistency_rate_over_planned = 0.7833`.
- SQLGlot combined same-engine coverage is lower on the full planned route denominator because generation failures, noop rows, and unsupported rows remain explicit.
- SQLGlot route-level attempted-denominator performance is still strong once a row reaches execution: `0.8667` on optimize and `0.9231` on transpile/noop.
- R-Bot generated only `7 / 120` rows, but all `7 / 7` generated PostgreSQL rows passed exact-match execution validity.
- R-Bot therefore has perfect subset validity on `generated_pg7_only`, but only `0.0583` validity coverage over the full `120`-row generation denominator.

### Speedup

- Direct LLM currently has the strongest single-route same-engine `GM_Speedup` in this comparison: `1.0436`.
- SQLGlot combined same-engine `GM_Speedup` is `1.0179`, with route-level values `1.0168` and `1.0190`.
- Direct LLM also has the lowest overall `RegressionRate@20%` in the comparison slice: `0.0319` versus SQLGlot combined `0.0511`.
- R-Bot PG7-only `GM_Speedup` is `0.947444` with `RegressionRate@20% = 0.2857`, but this is computed on only `7` timing-success PostgreSQL rows and is not comparable to fuller-denominator rows unless that scope difference is stated.

### PORT caveats

- PORT rows remain explicit portability-stress rows in both method families.
- No `SpeedupTransferRate` is computed here.
- Same-engine speedup evidence must not be reinterpreted as cross-engine portability benefit evidence.

## Boundaries

- This file is a denominator-aware method comparison summary.
- It is better described as a **pre-leaderboard** than a final leaderboard.
- It does not merge support-track metrics into method ranking.
- It does not include prior bounded-denominator methods except as old-denominator evidence in the separate ledger.
- It includes R-Bot only with explicit denominator labels because the retained timing slice is `generated_pg7_match_exact_only`, not full `120`-row timing and not tri-engine timing.
- A broader SQLGlot versus Direct LLM leaderboard, if desired later, should be built from explicit raw tables with route-normalized denominator policy rather than from markdown summaries alone.
