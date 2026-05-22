# SQLGlot Same-Engine 120 Readiness Audit v1

## Scope

This is a read-only audit of retained SQLGlot same-engine evidence for the
`common_core_v0_40_same_engine_120` denominator.

In scope:

- `sqlglot_transpile_same_dialect_noop`
- `sqlglot_optimize_same_dialect`
- `40` Common-core cases x `3` engines = `120` planned rows per route

Out of scope:

- new generation
- new execution
- new checker runs
- timing or speedup reruns
- SQL repair
- leaderboard updates
- `method_comparison_summary_v2` updates

## Headline Answer

Retained SQLGlot same-engine evidence is already route-separated and
paper-facing, but only as route-level appendix evidence:

- `sqlglot_transpile_same_dialect_noop`
  - planned `120`
  - generated `78`
  - source executed `78`
  - generated executed `78`
  - exact-match `72`
  - timing `72`
  - current status: `appendix_only`
- `sqlglot_optimize_same_dialect`
  - planned `120`
  - generated `75`
  - source executed `75`
  - generated executed `75`
  - exact-match `65`
  - timing `65`
  - current status: `appendix_only`

Neither route is currently suitable for a main leaderboard-style table row.

## Route Separation Audit

SQLGlot same-engine evidence is retained as two distinct routes, not as two
distinct methods:

- shared `method_id = sqlglot`
- distinct `route_id` values:
  - `sqlglot_transpile_same_dialect_noop`
  - `sqlglot_optimize_same_dialect`
- distinct paper-facing result labels:
  - `sqlglot_transpile_same_dialect_noop_result_card_v1`
  - `sqlglot_optimize_same_dialect_result_card_v1`
- distinct denominator IDs:
  - `common_core_v0_40_same_engine_120_transpile_noop_route`
  - `common_core_v0_40_same_engine_120_optimize_route`

Important retained-artifact boundary:

- top-level route cards and proposed-row previews are distinct
- batch run roots are shared:
  - `runs/sqlglot_same_engine_generation_01`
  - `runs/sqlglot_same_engine_nonport_execution_01`
  - `runs/sqlglot_same_engine_port_execution_resolved_01`
  - `runs/sqlglot_same_engine_timing_01`

So route isolation exists in `route_id`, filenames, and result labels, but not
as completely separate top-level execution roots.

## Route Rollup

| route_id | denominator_id | planned_rows | generated_rows | source_executed_rows | generated_executed_rows | exact_match_rows | timing_rows | eligibility | next bounded action |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `sqlglot_transpile_same_dialect_noop` | `common_core_v0_40_same_engine_120_transpile_noop_route` | `120` | `78` | `78` | `78` | `72` | `72` | `appendix_only` | keep as retained route evidence; if recovery is desired, isolate the `6` Spark parse-failure rows only |
| `sqlglot_optimize_same_dialect` | `common_core_v0_40_same_engine_120_optimize_route` | `120` | `75` | `75` | `75` | `65` | `65` | `appendix_only` | keep as retained route evidence; if recovery is desired, isolate the `27` generation-failed rows and `10` executed-failure rows in a bounded optimize-only audit |

Row-count conventions used here:

- `generated_rows`, `generated_executed_rows`, `exact_match_rows`, and
  `timing_rows` follow the retained paper-facing route summaries
- `source_executed_rows` is aligned to the retained generated-execution attempt
  denominator for that route
- explicit `noop_generated` and `unsupported` rows remain in denominator
  accounting but are not counted as generated/executed exact rows

## Missing Rows And Failure Buckets

### `sqlglot_transpile_same_dialect_noop`

Retained failure / non-exact bucket rollup:

- `parse_error = 6`
- `unsupported = 42`
  - `noop_generated = 24`
  - `skipped_unsupported = 18`

Non-exact rows by `case_id:engine`:

- parse failures:
  - `PERF_0008:spark`
  - `PERF_0013:spark`
  - `PERF_0017:spark`
  - `PERF_0019:spark`
  - `PERF_0024:spark`
  - `PERF_0077:spark`
- explicit no-op rows:
  - `PERF_0007:pg`
  - `PERF_0007:mysql`
  - `PERF_0007:spark`
  - `PERF_0033:pg`
  - `PERF_0033:mysql`
  - `PERF_0033:spark`
  - `PERF_0054:pg`
  - `PERF_0054:mysql`
  - `PERF_0054:spark`
  - `CONS_0036:pg`
  - `CONS_0036:mysql`
  - `CONS_0036:spark`
  - `CONS_0037:pg`
  - `CONS_0037:mysql`
  - `CONS_0037:spark`
  - `PORT_0003:pg`
  - `PORT_0004:mysql`
  - `PORT_0005:pg`
  - `PORT_0008:pg`
  - `PORT_0012:pg`
  - `PORT_0013:mysql`
  - `PORT_0022:mysql`
  - `PORT_0024:mysql`
  - `PORT_0025:mysql`
- explicit unsupported rows:
  - `PORT_0003:mysql`
  - `PORT_0003:spark`
  - `PORT_0004:pg`
  - `PORT_0004:spark`
  - `PORT_0005:mysql`
  - `PORT_0005:spark`
  - `PORT_0008:mysql`
  - `PORT_0008:spark`
  - `PORT_0012:mysql`
  - `PORT_0012:spark`
  - `PORT_0013:pg`
  - `PORT_0013:spark`
  - `PORT_0022:pg`
  - `PORT_0022:spark`
  - `PORT_0024:pg`
  - `PORT_0024:spark`
  - `PORT_0025:pg`
  - `PORT_0025:spark`

Interpretation:

- this route is recoverable only in a very narrow sense
- the only bounded recoverable frontier visible from retained evidence is the
  `6` Spark parse-failure rows
- the `24` no-op rows and `18` unsupported rows are already explicit denominator
  outcomes, not hidden debt

### `sqlglot_optimize_same_dialect`

Retained failure / non-exact bucket rollup:

- `generation_failed = 27`
- `executed_failed = 10`
  - `method_generated_sql_execution_failure = 9`
  - `engine_dialect_parse_failure = 1`
- `unsupported = 18`
- retained PORT execution-only rows without exact-check support = `9`

Non-exact rows by `case_id:engine`:

- execution failures from generated SQL:
  - `CONS_0005:pg`
  - `CONS_0005:mysql`
  - `CONS_0005:spark`
  - `CONS_0007:pg`
  - `CONS_0007:mysql`
  - `CONS_0007:spark`
  - `CONS_0009:pg`
  - `CONS_0009:mysql`
  - `CONS_0009:spark`
  - `PERF_0077:spark`
- generation failures:
  - `PERF_0008:pg`
  - `PERF_0008:mysql`
  - `PERF_0008:spark`
  - `PERF_0013:pg`
  - `PERF_0013:mysql`
  - `PERF_0013:spark`
  - `PERF_0017:pg`
  - `PERF_0017:mysql`
  - `PERF_0017:spark`
  - `PERF_0019:pg`
  - `PERF_0019:mysql`
  - `PERF_0019:spark`
  - `PERF_0024:pg`
  - `PERF_0024:mysql`
  - `PERF_0024:spark`
  - `PERF_0052:pg`
  - `PERF_0052:mysql`
  - `PERF_0052:spark`
  - `PERF_0054:pg`
  - `PERF_0054:mysql`
  - `PERF_0054:spark`
  - `PERF_0062:pg`
  - `PERF_0062:mysql`
  - `PERF_0062:spark`
  - `CONS_0024:pg`
  - `CONS_0024:mysql`
  - `CONS_0024:spark`
- explicit unsupported rows:
  - `PORT_0003:mysql`
  - `PORT_0003:spark`
  - `PORT_0004:pg`
  - `PORT_0004:spark`
  - `PORT_0005:mysql`
  - `PORT_0005:spark`
  - `PORT_0008:mysql`
  - `PORT_0008:spark`
  - `PORT_0012:mysql`
  - `PORT_0012:spark`
  - `PORT_0013:pg`
  - `PORT_0013:spark`
  - `PORT_0022:pg`
  - `PORT_0022:spark`
  - `PORT_0024:pg`
  - `PORT_0024:spark`
  - `PORT_0025:pg`
  - `PORT_0025:spark`
- PORT execution-only rows with no retained exact checker:
  - `PORT_0003:pg`
  - `PORT_0004:mysql`
  - `PORT_0005:pg`
  - `PORT_0008:pg`
  - `PORT_0012:pg`
  - `PORT_0013:mysql`
  - `PORT_0022:mysql`
  - `PORT_0024:mysql`
  - `PORT_0025:mysql`

Interpretation:

- this route is not “fully blocked”, but it is materially weaker than the
  transpile/no-op route
- the cleanest bounded recovery frontier is a separate optimize-only failure
  audit over:
  - `27` generation-failed rows
  - `10` executed-failure rows
- retained PORT execution-only rows should remain explicit and separate from
  exact-match counting

## Eligibility Decision

Using the current retained governance style:

- `sqlglot_transpile_same_dialect_noop` = `appendix_only`
- `sqlglot_optimize_same_dialect` = `appendix_only`

Reason:

- both already have retained denominator-aware route evidence
- both are already explicitly marked `leaderboard_comparable = no`
- both are held in the freeze ledger as route-level evidence rather than as a
  SQLGlot method-family aggregate
- PORT rows are still mixed into denominator accounting through explicit
  unsupported or execution-only boundaries

This audit does not support promoting either route into a new main-table claim.

## Exact Next Bounded Actions

- `sqlglot_transpile_same_dialect_noop`
  - no recovery is required to preserve the retained route packet
  - if additional recovery is approved later, restrict it to the `6` Spark
    parse-failure rows only
- `sqlglot_optimize_same_dialect`
  - if recovery is approved later, open a bounded optimize-only audit covering:
    - `27` generation-failed rows
    - `10` generated execution-failure rows
  - keep PORT execution-only evidence separate from exact-match claims

## Non-Claims

- This audit does not run new SQLGlot generation.
- This audit does not run new execution or checker work.
- This audit does not create timing or speedup claims.
- This audit does not repair SQL.
- This audit does not update `method_comparison_summary_v2`.
- This audit does not create or update a leaderboard row.
- This audit does not create a new result card.
