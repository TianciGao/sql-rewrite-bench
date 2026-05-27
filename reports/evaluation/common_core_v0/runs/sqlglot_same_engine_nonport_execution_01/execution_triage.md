**Execution Triage**
This is a read-only triage of the broader non-PORT SQLGlot same-engine execution package. It uses the live `run_results.json`, stderr logs, and the generation ledger to classify executed failures separately from preserved generation-failed and no-op rows.

Totals:
- total planned rows: `186`
- total records in `run_results.json`: `187`
- executed rows: `144`
- executed success count: `128`
- executed failure count: `16`
- `not_executed_generation_failed` count: `27`
- `noop_generated` count: `15`

Counts by pool:
- `consistency`: `54`
- `longtail`: `36`
- `performance`: `96`

Counts by engine:
- `mysql`: `62`
- `pg`: `62`
- `spark`: `62`

Counts by route:
- `sqlglot_optimize_same_dialect`: `93`
- `sqlglot_transpile_same_dialect_noop`: `93`

Outcome counts:
- `executed_failed`: `16`
- `executed_success`: `128`
- `not_executed_generation_failed`: `27`
- `noop_generated`: `15`

**Failed Rows**
- `CONS_0005 / mysql / sqlglot_optimize_same_dialect`: Bad generated reference shape table1.table2.i
- `CONS_0005 / pg / sqlglot_optimize_same_dialect`: Bad generated reference shape `table1.table2.i`
- `CONS_0005 / spark / sqlglot_optimize_same_dialect`: Bad generated reference shape table1.table2.i
- `CONS_0007 / mysql / sqlglot_optimize_same_dialect`: Bad generated reference shape e2.e1.commission
- `CONS_0007 / pg / sqlglot_optimize_same_dialect`: Bad generated reference shape `e2.e1.commission`
- `CONS_0007 / spark / sqlglot_optimize_same_dialect`: Bad generated reference shape e2.e1.commission
- `CONS_0009 / mysql / sqlglot_optimize_same_dialect`: Bad generated reference shape `t1.t0a`
- `CONS_0009 / pg / sqlglot_optimize_same_dialect`: Bad generated reference shape `t1.t0a`
- `CONS_0009 / spark / sqlglot_optimize_same_dialect`: Bad generated reference shape `t1.t0a`
- `PERF_0008 / spark / sqlglot_transpile_same_dialect_noop`: Spark parse syntax error near end of input
- `PERF_0013 / spark / sqlglot_transpile_same_dialect_noop`: Spark parse syntax error near end of input
- `PERF_0017 / spark / sqlglot_transpile_same_dialect_noop`: Spark parse syntax error near end of input
- `PERF_0019 / spark / sqlglot_transpile_same_dialect_noop`: Spark parse syntax error near end of input
- `PERF_0024 / spark / sqlglot_transpile_same_dialect_noop`: Spark parse syntax error near end of input
- `PERF_0077 / spark / sqlglot_optimize_same_dialect`: Spark parse syntax error near end of input
- `PERF_0077 / spark / sqlglot_transpile_same_dialect_noop`: Spark parse syntax error near end of input

**Top Error Patterns**
- `spark_parse_syntax_error`: `7`
- `bad_ref_t1.t0a`: `3`
- `bad_ref_table1.table2.i`: `3`
- `bad_ref_e2.e1.commission`: `3`

Interpretation:
- The previous MySQL runner/auth/database/table-state failures remain resolved. No failure in this broader run shows MySQL access-denied, create/drop-database permission, or leaked-table-state signatures.
- MySQL runner remains clean after the canary fix. The three MySQL failures are method SQL failures, not runner failures.
- Failures split into two dominant classes:
  - `9` consistency optimize failures on `CONS_0005`, `CONS_0007`, and `CONS_0009` across `pg/mysql/spark`. These are SQLGlot-generated SQL execution failures with bad nested reference shapes such as `e2.e1.commission`, `table1.table2.i`, and `t1.t0a`.
  - `7` Spark-only failures on performance rows, dominated by `PARSE_SYNTAX_ERROR` on generated or same-dialect no-op SQL. This is best treated as an engine dialect / parser compatibility failure class, not a runner failure.
- Failures are concentrated in `sqlglot_optimize_same_dialect` overall (`10` of `16` executed failures), but there is also a meaningful Spark parse-failure pocket on generated/no-op execution (`6` transpile/no-op failures plus `1` optimize failure on `PERF_0077`).
- Generation-failed rows and no-op rows are already preserved explicitly, which is the right denominator-aware behavior for this run package.

**Recommendation**
- `A.` Materialize the non-PORT execution package as denominator-aware method evidence.
- `B.` Preserve `generation_failed` rows explicitly.
- `C.` Preserve `no-op` rows explicitly.
- `D.` Do not compute speedup or a final leaderboard yet.
- `E.` Do not include `PORT` yet.
