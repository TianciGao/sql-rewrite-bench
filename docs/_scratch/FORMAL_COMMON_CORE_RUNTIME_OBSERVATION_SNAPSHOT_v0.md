# FORMAL_COMMON_CORE_RUNTIME_OBSERVATION_SNAPSHOT_v0

## Status

This is a tracked scratch summary of formal common-core runtime observation from existing execution reports only.

## Input Reports

- `reports/formal_common_core/native_identity_execution_v0.json`
- `reports/formal_common_core/human_reference_positive_execution_v0.json`
- `reports/formal_common_core/hard_negative_guard_execution_v0.json`
- `reports/formal_common_core/sqlglot_opt_same_dialect_execution_v0.json`
- `reports/formal_common_core/llm_direct_rewrite_execution_v0.json`
- `reports/formal_common_core/runtime_observation_snapshot_v0.json`

## Runtime Availability By Route

Runtime availability is complete across the 9-case denominator:

- native runtime available: `9 / 9`
- human positive runtime available: `9 / 9`
- hard negative runtime available: `9 / 9`
- SQLGlot runtime available: `9 / 9`
- Direct LLM runtime available: `9 / 9`

## Observed Single-Run Ratio Summary

Observed single-run ratios are available for all 9 cases in each source-relative comparison:

- human positive vs native: `9 / 9`
- hard negative vs native: `9 / 9`
- SQLGlot vs native: `9 / 9`
- Direct LLM vs native: `9 / 9`

Selected observations:

- `PERF_0006`: SQLGlot vs native `0.4601`, LLM vs native `0.2723`, human positive vs native `0.5634`, hard negative vs native `0.5117`
- `PERF_0013`: human positive vs native `2.7931`, SQLGlot vs native `0.9828`, LLM vs native `1.0517`
- `PERF_0033`: hard negative vs native `2.8421`, SQLGlot vs native `1.0`, human positive vs native `1.0`
- `PERF_0054`: human positive vs native `3.0351`, SQLGlot vs native `1.0175`, LLM vs native `1.0526`

## Strong Boundary

- this is not GM speedup
- this is not formal speedup
- there is no repeated measurement policy
- there is no warmup policy
- there is no timeout policy freeze
- the ratios are observed single-run runtime ratios only

## Next Action

- define repeat / warmup / timeout policy before formal speedup scoring
