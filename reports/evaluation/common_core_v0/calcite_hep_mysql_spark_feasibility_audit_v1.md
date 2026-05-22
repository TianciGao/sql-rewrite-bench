# Calcite HEP MySQL/Spark Feasibility Audit v1

## Scope

This is a bounded feasibility audit for extending the current Calcite HEP
baseline beyond the retained PostgreSQL-only path. It does **not** claim
MySQL/Spark support. It only determines whether a six-row rewrite canary is
justified and what blocker should stop that canary if the current wrapper
cannot safely target non-PG dialects.

## Selected canary rows

- `PERF_0006:mysql`
- `PERF_0006:spark`
- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

## Artifact coverage for selected rows

All three selected cases have the required same-engine inputs:

- `source.sql`: present
- `schema/ddl_mysql.sql`: present
- `schema/ddl_spark.sql`: present
- `validation/mysql_witness_data.sql`: present
- `validation/spark_witness_data.sql`: present

So the six-row canary is **not** blocked by missing schema or witness files.

## What the current Calcite HEP runner does

The retained PostgreSQL generation runner is wrapper-based:

- shell entrypoint:
  - `reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01/run_manual_calcite_hep_pg40_generation.sh`
- Java wrapper:
  - `tools/calcite_hep/CalciteHepRewriteSmoke.java`

The visible wrapper behavior is currently PostgreSQL-shaped:

1. parser config:
   - uses `SqlParser.config().withLex(Lex.MYSQL)`
2. SQL rendering:
   - uses `RelToSqlConverter(new PostgresqlSqlDialect.DEFAULT)`
   - renders with `toSqlString(PostgresqlSqlDialect.DEFAULT)`
3. route contract:
   - retained package is explicitly `calcite_hep_pg_rewrite`
   - current paper-facing summary is explicitly PG-only

## Design vs harness scope

Current best classification:

- the retained **benchmark evidence** is PostgreSQL-only by package scope
- the visible **wrapper implementation** is also PostgreSQL-shaped at output

That means this is not just a matrix omission. The current wrapper would need a
separate target-engine rendering decision before a MySQL/Spark canary could be
treated as same-engine evidence.

## Output-dialect conclusion

The visible wrapper does **not** currently prove same-engine MySQL or Spark
rewrite output.

Current observable behavior:

- parse path uses MySQL-style lexing
- output path uses PostgreSQL dialect rendering

So the current output should be treated as:

- `PG-like / PostgreSQL-dialect Calcite output`

not:

- `guaranteed MySQL output`
- `guaranteed Spark SQL output`

## Expected risks for MySQL/Spark

- parser support:
  - parser currently uses `Lex.MYSQL`, which may not match Spark syntax
- dialect rendering:
  - current wrapper emits PostgreSQL-shaped SQL, not engine-specific SQL
- date/time literal syntax:
  - may remain PostgreSQL-style after rewrite
- interval syntax:
  - likely engine-mismatched for MySQL or Spark in some cases
- anti-join / `NOT IN` semantics:
  - rewrite may be logically shaped through Calcite, but later execution
    compatibility remains unproven
- generated SQL extraction:
  - current package structure can capture emitted SQL safely
- target-engine execution compatibility:
  - cannot be assumed from rewrite generation alone

## Is a 6-row rewrite canary justified?

Yes, but only as a **fail-closed rewrite canary package**.

Reason:

- selected rows have all required case artifacts
- wrapper can be inspected and invoked in a bounded package
- current blocker is clear and package-level:
  - output dialect is still hard-coded to PostgreSQL

## Safe conclusion

The right next step is a six-row rewrite canary package that:

- keeps `mysql` and `spark` labels explicit
- does **not** execute SQL
- does **not** time anything
- fails closed if the wrapper still renders via `PostgresqlSqlDialect`
- does **not** silently use PG-shaped output as same-engine evidence
