# Calcite HEP MySQL/Spark Rewrite Canary v2 Triage

This is a read-only triage for the retained
`calcite_hep_mysql_spark_canary_02` result. It is rewrite-only evidence. It is
not execution evidence, not correctness evidence, not timing evidence, not
speedup evidence, and not leaderboard evidence.

## Headline Status

- planned rows = `6`
- rewrite_success rows = `6`
- failed rows = `0`
- preflight_blocked rows = `0`
- wrapper_compile_status = `ok`
- target_dialect_availability.mysql = `true`
- target_dialect_availability.spark = `true`

## Counts

By engine:

- `mysql = 3 rewrite_success`
- `spark = 3 rewrite_success`

By case:

- `PERF_0006 = 2 rewrite_success`
- `PERF_0007 = 2 rewrite_success`
- `CONS_0005 = 2 rewrite_success`

## Row-Level Outcome

All six rows succeeded as bounded rewrite outputs:

- `PERF_0006:mysql`
- `PERF_0006:spark`
- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

Per-row dialect class used:

- MySQL rows:
  - `org.apache.calcite.sql.dialect.MysqlSqlDialect`
- Spark rows:
  - `org.apache.calcite.sql.dialect.SparkSqlDialect`

Per-row `rewrite_changed`:

- `PERF_0006:mysql = true`
- `PERF_0006:spark = true`
- `PERF_0007:mysql = true`
- `PERF_0007:spark = true`
- `CONS_0005:mysql = true`
- `CONS_0005:spark = true`

## Artifact Presence

Generated SQL files:

- present for all `6 / 6` rows
- nonempty for all `6 / 6` rows

Other retained row artifacts:

- stdout logs present for all `6 / 6` rows
- stderr logs present for all `6 / 6` rows
- row metadata present for all `6 / 6` rows

## Rewrite Pipeline Status

From retained stdout metadata, all six rows report:

- `source_sql_accepted = true`
- `ddl_accepted = true`
- `schema_ddl_ingestion_succeeded = true`
- `calcite_parse_succeeded = true`
- `validation_succeeded = true`
- `sql_to_rel_succeeded = true`
- `hep_planner_succeeded = true`
- `rel_to_sql_succeeded = true`
- `dialect_rendering_status = target_dialect_rendered`

stderr does not contain a Java exception or SQL failure trace. The retained
stderr files contain only SLF4J no-op logger warnings.

## Did The Package Use Target Dialects Rather Than PostgreSQL Fallback?

Best retained evidence: yes, the package used explicit target dialect classes
rather than the old PostgreSQL fallback path.

Supporting observations:

- `dialect_class_used` is MySQL for all MySQL rows and Spark for all Spark rows
- MySQL and Spark outputs differ on the same case for `PERF_0006` and
  `PERF_0007`
- Spark output contains Spark-shaped ordering text such as `NULLS LAST`
- no visible PostgreSQL-only renderer is reported in row metadata

## Obvious SQL Surface Caveats

No obvious PostgreSQL-only markers such as these were observed in the generated
SQL:

- `::` casts
- `ILIKE`
- `SERIAL`
- `RETURNING`

However, rewrite-only success is not execution validity. The generated SQL still
contains syntax that may need engine-side validation before any correctness
claim, including:

- standard `DATE '...'` literals
- `INTERVAL '1' YEAR`
- Spark rows with `NULLS LAST`

So this canary shows target-dialect rendering attempts succeeded, but it does
not show that MySQL or Spark will execute the emitted SQL correctly.

## Metadata Hygiene Caveat

There is a retained metadata hygiene issue:

- `run_event_long.csv` leaves `schema_path` blank for all rows
- row metadata also records `schema_path = null`
- this is inconsistent with the retained wrapper stdout, which reports
  `schema_ddl_ingestion_succeeded = true`

This is a metadata completeness issue, not a rewrite blocker.

There is also an adjacent artifact-path hygiene issue in retained package-level
records:

- `log_stderr_path` is blank in `run_event_long.csv` and `run_results.json`
- but the stderr log files do exist on disk

## Boundary

This result is:

- rewrite-only canary evidence
- not execution evidence
- not correctness / result-consistency evidence
- not timing evidence
- not speedup evidence

Existing Calcite HEP PG-only canonical evidence remains unchanged until a later
separate MySQL/Spark execution or validity package is created and completed.

## Recommended Next Step

A bounded MySQL/Spark execution/validity canary package is justified next.

Reason:

- package-level wrapper and target-dialect blockers are now cleared
- all `6 / 6` rows produced nonempty target-dialect SQL
- rewrite-only evidence now exists for both MySQL and Spark

But the next package should stay tightly bounded to these same six rows and must
make the claim boundary explicit:

- execution-only / validity-only
- no timing
- no speedup
- no method-comparison update

Until that execution step exists, MySQL/Spark correctness remains not computed
for Calcite HEP.
