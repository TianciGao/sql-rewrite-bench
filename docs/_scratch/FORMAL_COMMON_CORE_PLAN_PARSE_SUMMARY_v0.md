# FORMAL_COMMON_CORE_PLAN_PARSE_SUMMARY_v0

## Status

This is a tracked scratch summary of formal common-core plan parse and route-pair readiness from existing PostgreSQL plan JSON artifacts.

## Input Plan Artifacts

The current summary reads only existing plan artifacts:

- `cases/<POOL>/<CASE>/runs/pg/plans/source.json`
- `cases/<POOL>/<CASE>/runs/pg/plans/rewrite_pos_01.json`
- `cases/<POOL>/<CASE>/runs/pg/plans/rewrite_neg_01.json`
- `cases/<POOL>/<CASE>/runs/pg/plans/plan_check.json`
- `reports/formal_common_core/plans/sqlglot_opt_same_dialect/<case_id_lower>.json`
- `reports/formal_common_core/plans/llm_direct_rewrite/<case_id_lower>.json`
- `reports/formal_common_core/plan_parse_summary_v0.json`

## Plan Parse Readiness By Role

Current parse readiness is complete across all five plan roles in the 9-case denominator:

- source plans parseable: `9 / 9`
- human positive plans parseable: `9 / 9`
- hard negative plans parseable: `9 / 9`
- SQLGlot method plans parseable: `9 / 9`
- Direct LLM method plans parseable: `9 / 9`

## Pair Readiness By Route

Current source-paired readiness is complete across all inspected route pairs:

- source-positive pair ready: `9 / 9`
- source-negative pair ready: `9 / 9`
- source-SQLGlot pair ready: `9 / 9`
- source-LLM pair ready: `9 / 9`

This means the current artifact layer is ready for a later pairwise operator-delta preflight.

## Basic Operator / Node-Type Observations

Basic plan-node extraction succeeded on the current PostgreSQL JSON structure.

Observed examples from the parsed report:

- `PERF_0006`: top node `Sort`; node types include `Aggregate`, `Seq Scan`, `Sort`
- `PERF_0008`: top node `Limit`; node types include `Aggregate`, `Hash`, `Hash Join`, `Seq Scan`, `Sort`
- `PERF_0013`: top node `Sort`; node types include `Aggregate`, `Hash`, `Hash Join`, `Index Scan`, `Nested Loop`, `Seq Scan`, `Sort`
- `PERF_0054`: node types include `Incremental Sort`
- `CONS_0007`: source and SQLGlot plans reduce to `Seq Scan`, while positive / negative / LLM include `Hash Join` and `Aggregate`
- `CONS_0012`: source, SQLGlot, and LLM plans include `Limit` and `Seq Scan`, while positive / negative include `Hash Join` and `Aggregate`

## What Is Ready Now

- all source plans are parseable
- all control plans are parseable
- all generated-method plans are parseable
- all source-to-route plan pairs are ready
- `operator_delta_preflight_ready=true`

## What Remains Missing

- attribution is still not ready
- speedup scoring is still not ready
- operator delta and attribution still require a separate command
- runtime and speedup policy are still not frozen

## Claim Boundaries

- no EXPLAIN was run
- no SQL was executed
- no new plans were collected
- plan parse readiness is not speedup scoring
- plan pair readiness is not attribution
- operator delta and attribution still require a separate command
- runtime / speedup policy is still not frozen

## Recommended Next Action

- implement formal plan operator-delta preflight for source-vs-SQLGlot and source-vs-Direct-LLM plan pairs
