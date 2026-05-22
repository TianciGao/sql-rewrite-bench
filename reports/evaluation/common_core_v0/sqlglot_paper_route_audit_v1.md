# SQLGlot Paper Route Audit v1

## Scope

This audit inventories the retained SQLGlot-related evidence under
`reports/evaluation/common_core_v0` and separates:

1. SQLGlot no-opt / normalize / parse-render route
2. SQLGlot optimize same-engine route
3. SQLGlot Transpile cross-dialect / portability route
4. LLM Translate cross-dialect / portability route, if present

This is an audit only. It does not update `method_comparison_summary_v2`, does
not update paper synthesis files, and does not execute any benchmark runs.

## Headline Answer

Retained paper-facing SQLGlot evidence already exists for **two same-engine
routes**:

- `sqlglot_optimize_same_dialect`
- `sqlglot_transpile_same_dialect_noop`

Both routes already appear in `method_comparison_summary_v2` as route-level
rows and are supported by retained validity and speedup summaries.

No retained dedicated paper-facing route was found for:

- a SQLGlot **cross-dialect portability** route, or
- a Direct LLM / LLM Translate **cross-dialect portability** route.

Those route families should remain out of the same-engine `120` method table
unless and until a separate PORT / cross-dialect evidence packet is built.

## Route Inventory

### 1. SQLGlot no-opt / normalize / parse-render route

Retained route:

- `route_id = sqlglot_transpile_same_dialect_noop`
- `method_id = sqlglot`
- `denominator_id = common_core_v0_40_same_engine_120_transpile_noop_route`

Retained counts:

- planned rows: `120`
- generated rows: `78`
- executed rows: `72`
- exact-match rows: `72`
- timing denominator: `timing_success_72_on_transpile_noop_route`
- leaderboard comparable: `no`

Evidence basis:

- `sqlglot_validity_summary_v1.md`
- `sqlglot_speedup_summary_v1.md`
- `method_comparison_summary_v2.md`

This route belongs in the same-engine `120` comparison discussion as a
**route-level row**, not as a cross-dialect portability row.

### 2. SQLGlot optimize same-engine route

Retained route:

- `route_id = sqlglot_optimize_same_dialect`
- `method_id = sqlglot`
- `denominator_id = common_core_v0_40_same_engine_120_optimize_route`

Retained counts:

- planned rows: `120`
- generated rows: `75`
- executed rows: `65`
- exact-match rows: `65`
- timing denominator: `timing_success_65_on_optimize_route`
- leaderboard comparable: `no`

Evidence basis:

- `sqlglot_validity_summary_v1.md`
- `sqlglot_speedup_summary_v1.md`
- `method_comparison_summary_v2.md`

This route also belongs in the same-engine `120` comparison discussion as a
**route-level row**.

### 3. SQLGlot Transpile cross-dialect / portability route

No retained dedicated route packet was found for a SQLGlot
cross-dialect portability route.

Important distinction:

- the retained `sqlglot_transpile_same_dialect_noop` route is still a
  **same-engine** route
- it includes explicit PORT rows in denominator accounting, but it is not a
  dedicated cross-dialect translation result packet

Therefore:

- same-engine `120` table: `no`
- separate PORT / cross-dialect table: `not ready`

Current missing artifacts:

- dedicated `route_id`
- retained route-level `run_results.json`
- denominator-aware validity summary for cross-dialect portability
- execution/exact-match packet for a cross-dialect denominator
- dedicated result card or proposed row

### 4. LLM Translate cross-dialect / portability route

No retained dedicated Direct LLM / LLM Translate cross-dialect portability
route was found.

The retained Direct LLM evidence under `common_core_v0` is:

- `route_id = direct_llm_same_engine_rewrite`
- `denominator_id = common_core_v0_40`
- same-engine only

Therefore:

- same-engine `120` table: only the retained `direct_llm_same_engine_rewrite`
  row, which already exists elsewhere
- separate PORT / cross-dialect table: `not ready`

Current missing artifacts:

- dedicated cross-dialect `route_id`
- retained portability generation / execution / exact-match packet
- denominator-aware cross-dialect result card or proposed row

## Paper-Facing Status By Route

### Already paper-facing

- `sqlglot_validity_summary_v1.md`
- `sqlglot_speedup_summary_v1.md`
- route-level SQLGlot rows in `method_comparison_summary_v2`

These already provide retained paper-facing route evidence, but they do not yet
have dedicated route result cards analogous to later Calcite HEP cards.

### Still missing denominator-aligned paper artifacts

For SQLGlot route-level promotion, the main missing artifact is not raw
evidence. It is a **dedicated paper-facing route card / proposed row** that
states the claim boundary cleanly.

For portability / cross-dialect SQLGlot and LLM Translate routes, the missing
artifacts are more fundamental:

- no retained dedicated route packet
- no dedicated denominator
- no retained route-level exact-match summary
- no paper-facing result card

## Recommendation

The next single SQLGlot route to promote into a paper-facing proposed row is:

- `sqlglot_transpile_same_dialect_noop`

Why this route:

- it already has retained denominator-aware validity evidence
- it already has retained timing evidence
- it uses a clean `120`-row same-engine route denominator
- it is stronger than `sqlglot_optimize_same_dialect` on retained exact-match
  coverage (`72/120` vs `65/120`)
- it is easier to explain than the combined `240`-row aggregate row

Recommended claim boundary:

`SQLGlot transpile_same_dialect_noop is a same-engine 120-row route-level evidence row. It should be reported as denominator-aware route evidence, not as a cross-dialect portability result, not as a leaderboard-comparable scalar, and not as a full-method-family aggregate row. Unsupported and noop rows remain explicit in denominator accounting.`

## Next Safe Action

Create a dedicated paper-facing proposed row or result card for:

- `method_id = sqlglot`
- `route_id = sqlglot_transpile_same_dialect_noop`
- `denominator_id = common_core_v0_40_same_engine_120_transpile_noop_route`

and keep cross-dialect portability reporting separate until a dedicated
PORT / cross-dialect route packet exists.
