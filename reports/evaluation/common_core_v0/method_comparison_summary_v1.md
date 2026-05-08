**Method Comparison Summary**
This is a coverage-aware SQLGlot versus Direct LLM same-engine method comparison summary for `common_core_v0_40`.

It should be treated as a **pre-leaderboard comparison**, not a final leaderboard.

Why this is not a final leaderboard:
- SQLGlot same-engine evidence spans **two explicit routes**: `sqlglot_optimize_same_dialect` and `sqlglot_transpile_same_dialect_noop`.
- Direct LLM same-engine evidence spans **one route**: `direct_llm_same_engine_rewrite`.
- SQLGlot therefore has a `240`-row planned same-engine route denominator, while Direct LLM has a `120`-row planned route denominator.
- Benchmark support / controls readiness, verifier-support, and plan-observability metrics remain separate from method ranking metrics.

Coverage-aware key comparison:

| method_group | route_id | planned_rows | attempted_or_ready_rows | executable_rate_planned | executable_rate_attempted_or_ready | result_consistency_rate_planned | result_consistency_rate_executed | timing_success_rows | coverage_planned | coverage_timing_eligible | GM_Speedup | RegressionRate@20% |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `sqlglot` | `sqlglot_combined_same_engine` | `240` | `153` | `0.5708` | `0.8954` | `0.5708` | `0.8954` | `137` | `0.5708` | `1.0000` | `1.0179` | `0.0511` |
| `sqlglot` | `sqlglot_optimize_same_dialect` | `120` | `75` | `0.5417` | `0.8667` | `0.5417` | `0.8667` | `65` | `0.5417` | `1.0000` | `1.0168` | `0.0615` |
| `sqlglot` | `sqlglot_transpile_same_dialect_noop` | `120` | `78` | `0.6000` | `0.9231` | `0.6000` | `0.9231` | `72` | `0.6000` | `1.0000` | `1.0190` | `0.0417` |
| `direct_llm` | `direct_llm_same_engine_rewrite` | `120` | `115` | `0.8250` | `0.8609` | `0.7833` | `0.9495` | `94` | `0.7833` | `1.0000` | `1.0436` | `0.0319` |

## Interpretation

### Denominator differences

- SQLGlot combined same-engine reporting should not be read as “one route versus one route”. It is the aggregate of two distinct same-engine routes with different generation and skip behavior.
- Direct LLM is a single-route same-engine packet, so its `120` planned rows are structurally different from SQLGlot’s `240` combined rows.
- A route-to-route comparison is more defensible than a flattened method-family ranking.

### Validity and execution

- Direct LLM has the strongest single-route validity coverage in the current evidence: `executable_rate_over_planned = 0.8250` and `result_consistency_rate_over_planned = 0.7833`.
- SQLGlot combined same-engine coverage is lower on the full planned route denominator because generation failures, noop rows, and unsupported rows remain explicit.
- SQLGlot route-level attempted-denominator performance is still strong once a row reaches execution: `0.8667` on optimize and `0.9231` on transpile/noop.

### Speedup

- Direct LLM currently has the strongest single-route same-engine `GM_Speedup` in this comparison: `1.0436`.
- SQLGlot combined same-engine `GM_Speedup` is `1.0179`, with route-level values `1.0168` and `1.0190`.
- Direct LLM also has the lowest overall `RegressionRate@20%` in the comparison slice: `0.0319` versus SQLGlot combined `0.0511`.

### PORT caveats

- PORT rows remain explicit portability-stress rows in both method families.
- No `SpeedupTransferRate` is computed here.
- Same-engine speedup evidence must not be reinterpreted as cross-engine portability benefit evidence.

## Boundaries

- This file is a denominator-aware method comparison summary.
- It is better described as a **pre-leaderboard** than a final leaderboard.
- It does not merge support-track metrics into method ranking.
- It does not include prior bounded-denominator methods except as old-denominator evidence in the separate ledger.
- A broader SQLGlot versus Direct LLM leaderboard, if desired later, should be built from explicit raw tables with route-normalized denominator policy rather than from markdown summaries alone.
