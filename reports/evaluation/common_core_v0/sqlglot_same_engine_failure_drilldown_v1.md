# SQLGlot Same-Engine Failure Drilldown v1

## A. Executive Conclusion

- `sqlglot_transpile_same_dialect_noop` remains `appendix_only`.
- `sqlglot_optimize_same_dialect` remains `appendix_only`.
- These are two SQLGlot routes, not two independent methods.
- No `120`-row main-table SQLGlot evidence exists.

Why not:

- both retained packets are explicitly route-level, denominator-aware evidence
- both are already frozen as `leaderboard_comparable = no`
- the no-op/transpile route is partly a same-dialect control path rather than a
  rewrite-optimizer path
- the optimize route still carries material generation-failure, execution-failure,
  and PORT boundary debt

## B. Route Interpretation

### `sqlglot_transpile_same_dialect_noop`

This route is best understood as a same-dialect SQLGlot transpile/no-op control:

- parse source SQL
- render it back in the same target dialect
- preserve explicit no-op outcomes when normalized SQL is unchanged

That makes it useful appendix evidence for:

- dialect parser coverage
- same-dialect render stability
- denominator-aware no-op accounting

It is not the strongest representation of SQLGlot as a rewrite optimizer.

### `sqlglot_optimize_same_dialect`

This route is the actual SQLGlot optimization path:

- parse source SQL
- apply SQLGlot optimize logic
- emit same-dialect optimized SQL

It is the more method-like SQLGlot route, but it still fails to reach a clean
`120`-row exact-match package.

### Why keep them separate in appendix

They can be shown separately in appendix because they answer different
questions:

- `transpile_same_dialect_noop` asks whether SQLGlot can parse and re-render
  same-dialect SQL safely
- `optimize_same_dialect` asks whether SQLGlot’s optimizer path can produce
  executable and exact same-engine rewrites

They should not be treated as two main-table methods because:

- both share `method_id = sqlglot`
- both share batch generation / execution / timing roots
- route semantics are different enough that combining them as peer methods
  would overstate method-family evidence

## C. Failure Drilldown

## `sqlglot_transpile_same_dialect_noop`

Retained route totals:

- planned rows: `120`
- generated rows: `78`
- source executed rows: `78`
- generated executed rows: `78`
- exact-match rows: `72`
- timing rows: `72`

Failure / non-exact split:

- `parse_error = 6`
- `unsupported = 42`
  - `noop_generated = 24`
  - `skipped_unsupported = 18`

### Parse-error rows

All retained parse failures are Spark-only:

- `PERF_0008:spark`
- `PERF_0013:spark`
- `PERF_0017:spark`
- `PERF_0019:spark`
- `PERF_0024:spark`
- `PERF_0077:spark`

Interpretation:

- this is a bounded Spark-only failure frontier
- it does not threaten the retained appendix packet
- recovering these `6` rows would improve cleanliness, but would not change the
  route’s main-table status because the route would still remain:
  - a route-level SQLGlot control path
  - mixed with explicit no-op and unsupported denominator rows
  - non-leaderboard-comparable

### Unsupported vs no-op

Explicit no-op rows remain visible and should not be reinterpreted as exact
rewrite success:

- performance no-op examples:
  - `PERF_0007:{pg,mysql,spark}`
  - `PERF_0033:{pg,mysql,spark}`
  - `PERF_0054:{pg,mysql,spark}`
- consistency no-op examples:
  - `CONS_0036:{pg,mysql,spark}`
  - `CONS_0037:{pg,mysql,spark}`
- PORT no-op examples:
  - `PORT_0003:pg`
  - `PORT_0004:mysql`
  - `PORT_0005:pg`
  - `PORT_0008:pg`
  - `PORT_0012:pg`
  - `PORT_0013:mysql`
  - `PORT_0022:mysql`
  - `PORT_0024:mysql`
  - `PORT_0025:mysql`

Explicit unsupported rows are concentrated in PORT stress rows where the
control-native source or engine-route combination was preserved as unsupported
rather than silently dropped.

### Worth recovering?

Only narrowly.

Recommendation for this route:

- bounded recovery possible, but not worth doing for paper main table
- at most, recover the `6` Spark parse-error rows if the appendix needs cleaner
  per-engine row counts

## `sqlglot_optimize_same_dialect`

Retained route totals:

- planned rows: `120`
- generated rows: `75`
- source executed rows: `75`
- generated executed rows: `75`
- exact-match rows: `65`
- timing rows: `65`

Failure / non-exact split:

- `generation_failed_method_error = 27`
- `generated_execution_failure_method_generated_sql_execution_failure = 9`
- `generated_execution_failure_engine_dialect_parse_failure = 1`
- `unsupported = 18`
- `executed_no_exact_port_only = 9`

### Generation-failed rows

These are the largest debt cluster and appear across all three engines:

- `CONS_0024:{pg,mysql,spark}`
- `PERF_0008:{pg,mysql,spark}`
- `PERF_0013:{pg,mysql,spark}`
- `PERF_0017:{pg,mysql,spark}`
- `PERF_0019:{pg,mysql,spark}`
- `PERF_0024:{pg,mysql,spark}`
- `PERF_0052:{pg,mysql,spark}`
- `PERF_0054:{pg,mysql,spark}`
- `PERF_0062:{pg,mysql,spark}`

Interpretation:

- this is not a small cleanup frontier
- it is a multi-case optimize-path weakness
- recovering it would require a separate optimize-only engineering campaign, not
  a paper-only normalization pass

### Generated execution failures

Most executed failures are generated-SQL shape failures in the consistency
cluster:

- `CONS_0005:{pg,mysql,spark}`
  - retained top error: bad generated reference shape `table1.table2.i`
- `CONS_0007:{pg,mysql,spark}`
  - retained top error: bad generated reference shape `e2.e1.commission`
- `CONS_0009:{pg,mysql,spark}`
  - retained top error: bad generated reference shape `t1.t0a`

Plus one engine-specific parse failure:

- `PERF_0077:spark`
  - retained top error: Spark parse syntax error near end of input

Interpretation:

- these are not denominator bookkeeping artifacts
- they are substantive optimize-route generated SQL failures
- even if recovered, the route would still inherit the larger `27`-row
  generation-failure frontier

### Unsupported rows

Explicit unsupported rows are the `18` PORT combinations:

- MySQL unsupported:
  - `PORT_0003:mysql`
  - `PORT_0005:mysql`
  - `PORT_0008:mysql`
  - `PORT_0012:mysql`
- PostgreSQL unsupported:
  - `PORT_0004:pg`
  - `PORT_0013:pg`
  - `PORT_0022:pg`
  - `PORT_0024:pg`
  - `PORT_0025:pg`
- Spark unsupported:
  - `PORT_0003:spark`
  - `PORT_0004:spark`
  - `PORT_0005:spark`
  - `PORT_0008:spark`
  - `PORT_0012:spark`
  - `PORT_0013:spark`
  - `PORT_0022:spark`
  - `PORT_0024:spark`
  - `PORT_0025:spark`

These should stay explicit in denominator accounting.

### Executed-no-exact PORT-only rows

There are `9` retained PORT optimize rows that executed but do not have
retained exact-check support:

- `PORT_0003:pg`
- `PORT_0004:mysql`
- `PORT_0005:pg`
- `PORT_0008:pg`
- `PORT_0012:pg`
- `PORT_0013:mysql`
- `PORT_0022:mysql`
- `PORT_0024:mysql`
- `PORT_0025:mysql`

These are appendix boundary rows, not hidden exact-match successes.

### Worth recovering?

Not for the main table.

Recommendation for this route:

- bounded recovery possible but not worth doing for paper main table
- if any recovery is approved, it should be only to make appendix accounting
  cleaner:
  - one optimize-only generation-failure audit over the `27` method-error rows
  - one optimize-only execution-failure audit over the `10` executed-failure
    rows

Even a successful bounded cleanup would not turn this route into a clean
main-table SQLGlot row because:

- route-level framing would still remain
- shared SQLGlot family semantics would still remain
- PORT unsupported and execution-only boundary rows would still remain explicit

## D. Recovery Recommendation

`bounded recovery possible but not worth doing for paper main table`

Recommended practical stance:

- preserve both SQLGlot same-engine routes as appendix-only evidence
- do not spend recovery effort trying to make them main-table-eligible for this
  paper cycle
- only pursue bounded cleanup if appendix presentation specifically wants:
  - cleaner Spark accounting for `transpile_same_dialect_noop`
  - cleaner failure taxonomy for `optimize_same_dialect`

## E. Paper-Safe Wording

For `sqlglot_transpile_same_dialect_noop`:

`SQLGlot transpile_same_dialect_noop is retained as a same-engine route-level appendix packet over the 120-row common-core denominator. It captures denominator-aware exact rows, no-op rows, and explicit unsupported rows, but it is not a main-table SQLGlot method row and not leaderboard-comparable evidence.`

For `sqlglot_optimize_same_dialect`:

`SQLGlot optimize_same_dialect is retained as a same-engine route-level appendix packet over the 120-row common-core denominator. It provides bounded optimize-route evidence with explicit generation failures, generated-SQL execution failures, and unsupported PORT rows, but it is not a main-table SQLGlot method row and not leaderboard-comparable evidence.`

## F. Non-Claims

- No new SQLGlot generation was run.
- No PostgreSQL / MySQL / Spark execution was run.
- No checker, timing, or speedup work was run.
- No SQL was repaired.
- No leaderboard row was created.
- `method_comparison_summary_v2` remains unchanged.
