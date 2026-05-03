# FORMAL_COMMON_CORE_PLAN_OPERATOR_DELTA_PREFLIGHT_SUMMARY_v0

## Status

This is a tracked scratch summary of formal common-core plan operator-delta preflight from existing PostgreSQL plan artifacts.

## Inputs

The preflight reads only existing plan JSON artifacts:

- `cases/<POOL>/<CASE>/runs/pg/plans/source.json`
- `cases/<POOL>/<CASE>/runs/pg/plans/rewrite_pos_01.json`
- `cases/<POOL>/<CASE>/runs/pg/plans/rewrite_neg_01.json`
- `reports/formal_common_core/plans/sqlglot_opt_same_dialect/<case_id_lower>.json`
- `reports/formal_common_core/plans/llm_direct_rewrite/<case_id_lower>.json`
- `reports/formal_common_core/plan_operator_delta_preflight_v0.json`

## Pair Readiness Summary

Current pair readiness is complete across all inspected source-paired routes:

- total pairs: `36`
- ready pairs: `36`
- blocked pairs: `0`
- source-positive ready: `9 / 9`
- source-negative ready: `9 / 9`
- source-SQLGlot ready: `9 / 9`
- source-LLM ready: `9 / 9`

## Lightweight Node / Operator Observations

The current preflight only records lightweight operator-delta observations.

Observed route-level signals:

- top-node changed count:
  - source-positive: `2`
  - source-negative: `2`
  - source-SQLGlot: `0`
  - source-LLM: `1`
- node-type delta available count:
  - source-positive: `9`
  - source-negative: `9`
  - source-SQLGlot: `9`
  - source-LLM: `9`

Observed examples:

- `PERF_0006`: all four source-paired routes keep the same top node `Sort`
- `PERF_0008`: all four source-paired routes keep the same top node `Limit`
- `CONS_0007`: source-positive and source-negative add `Aggregate`, `Hash`, and `Hash Join` relative to the source plan; source-LLM adds `Hash` and `Hash Join`; source-SQLGlot shows no node-type delta
- `CONS_0012`: source-positive and source-negative add `Aggregate`, `Hash`, and `Hash Join` and remove `Limit`; source-SQLGlot and source-LLM match the source node-type set

## Boundaries

- no attribution
- no speedup
- no EXPLAIN
- no SQL execution
- no performance explanation claim

## Next Action

- implement formal plan operator-delta summary / attribution design only after reviewing this preflight
