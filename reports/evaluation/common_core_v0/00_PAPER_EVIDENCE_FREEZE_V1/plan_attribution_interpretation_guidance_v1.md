# Plan Attribution Interpretation Guidance V1

This note explains how to present the reviewed 24-row PostgreSQL attribution packet safely in the paper.

## What This Packet Shows

- 24/24 reviewed PG rows have source and rewrite EXPLAIN ANALYZE BUFFERS JSON plans.
- 21/24 rows are `buffer_or_runtime_delta_without_operator_change`.
- 22/24 rows are `low` confidence and only 2/24 rows are `medium` confidence.
- The packet is still useful because it shows that scalar speedup labels alone do not explain why a rewrite helped, hurt, or tied.

## Recommended Table 10 V5 Case Set

- `sqlglot__sqlglot_optimize_same_dialect__PERF_0082__pg` (join_strategy_change, medium)
- `calcite_hep__calcite_hep_fail_closed_120__LONGTAIL_0013__pg` (node_count_change, medium)
- `sqlglot__sqlglot_optimize_same_dialect__LONGTAIL_0011__pg` (scan_strategy_change, low)
- `sqlglot__sqlglot_transpile_same_dialect_noop__PERF_0017__pg` (buffer_or_runtime_delta_without_operator_change, low)
- `direct_llm__direct_llm_same_engine_rewrite__PERF_0008__pg` (buffer_or_runtime_delta_without_operator_change, low)
- `direct_llm__direct_llm_execute_repair_1shot__LONGTAIL_0023__pg` (buffer_or_runtime_delta_without_operator_change, low)

## Safe Paper Framing

- Use this packet as selected-case PG plan-attribution evidence only.
- Say that route-level observability is stronger than scalar labels alone because SQL artifacts, ledgers, timing traces, and selected plan/runtime/buffer evidence are retained.
- Say explicitly that most rows remain low-confidence and buffer/runtime-only, so stronger denominator-wide attribution is still future work.

## What Must Not Be Overclaimed

- Do not claim global causal attribution.
- Do not claim denominator-wide node alignment coverage.
- Do not claim that the 24-row PG packet replaces Table 6 timing.
- Do not present low-confidence buffer/runtime-only rows as decisive operator-level explanations.

中文说明：这个 packet 的价值在于“可观察性增强”，不是“已经完成全量归因”。
