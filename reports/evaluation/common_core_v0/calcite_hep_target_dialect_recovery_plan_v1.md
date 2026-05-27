# Calcite HEP Target-Dialect Recovery Plan v1

## Goal

Move the bounded Calcite HEP MySQL/Spark canary from the retained
`target_engine_dialect_not_implemented` preflight stop in
`calcite_hep_mysql_spark_canary_01` to actual bounded rewrite attempts where
safe.

This plan is still canary-only:

- no SQL execution
- no correctness claim
- no timing
- no speedup
- no method-comparison update

## Retained blocker from canary 01

The retained canary 01 preflight failed because the visible shared wrapper:

- rendered through `PostgresqlSqlDialect`
- exposed no explicit `MysqlSqlDialect` route
- exposed no explicit `SparkSqlDialect` route

That blocker was wrapper-local, not artifact-local.

## What the visible Calcite checkout provides

The visible Calcite checkout contains direct dialect classes under
`core/src/main/java/org/apache/calcite/sql/dialect/`:

- `MysqlSqlDialect.java`
- `SparkSqlDialect.java`
- `PostgresqlSqlDialect.java`
- `HiveSqlDialect.java`

This means a bounded package-local wrapper can safely probe:

- `MysqlSqlDialect.DEFAULT`
- `SparkSqlDialect.DEFAULT`

without modifying the canonical PG wrapper.

## Recovery policy

The recovery package uses a package-local Java wrapper source and does not edit
`tools/calcite_hep/CalciteHepRewriteSmoke.java`.

Policy:

1. MySQL rows:
   - attempt `MysqlSqlDialect.DEFAULT`
2. Spark rows:
   - attempt `SparkSqlDialect.DEFAULT`
3. No PostgreSQL fallback:
   - do not silently render MySQL or Spark rows through
     `PostgresqlSqlDialect`
4. No SQLGlot transpilation:
   - do not contaminate Calcite HEP with SQLGlot-based target rendering
5. No Hive approximation by default:
   - `HiveSqlDialect` is not used as a Spark substitute in v2
   - if `SparkSqlDialect` is unavailable or the wrapper cannot compile, Spark
     rows must fail closed

## Expected remaining risks

- parser support:
  - parse still may fail on dialect-specific syntax
- validation / sql-to-rel:
  - Calcite may reject some same-engine syntax even if parsing succeeds
- HEP rewrite:
  - rewrite may fail after validation
- rel-to-sql:
  - target dialect may still emit SQL that is nonempty but later not execution
    compatible

Those are valid canary findings. They are different from the earlier package
blocker and should be surfaced as row-level rewrite outcomes if reached.

## Planned v2 boundary

The v2 canary may establish only:

- target-engine dialect class availability
- package-local wrapper compile success or failure
- bounded rewrite attempt outcomes for 6 rows
- whether final target-engine SQL was rendered and nonempty
- whether the emitted SQL is a noop or changed rewrite

It must not establish:

- execution validity
- correctness
- timing
- speedup
- tri-engine support

## Safe next step

Create `calcite_hep_mysql_spark_canary_02` as a bounded rewrite-only package
with:

- explicit engine labels
- explicit dialect class recording per row
- engine-by-engine preflight blocking
- package-local wrapper source
- no mutation of canonical PG evidence or comparison ledgers
