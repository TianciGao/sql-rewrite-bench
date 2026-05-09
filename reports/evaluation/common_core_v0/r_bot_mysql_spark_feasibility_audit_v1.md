# R-Bot MySQL/Spark Feasibility Audit v1

## Scope

This is a bounded, read-only audit for extending the recovered formal R-Bot harness beyond PostgreSQL under the `common_core_v0` same-engine protocol. It does **not** claim MySQL or Spark support. It only determines whether a six-row generation canary is justified and what blockers remain before any human-run attempt.

## Current state

- Latest retained R-Bot comparison evidence is PostgreSQL-only:
  - PG40 generation expansion: `15 generated / 25 failed / 0 blocked / 0 unsupported`
  - PG15 execution expansion: `15 executed / 15 match_exact`
  - PG15 timing expansion: `GM_Speedup = 0.921825`, `RegressionRate@20% = 20.00%`
- Earlier formal `@120` evidence marked all `80` MySQL/Spark rows unsupported.
- The newer PostgreSQL expansion audit shows that the old `unsupported` classification came from a recovered-harness route boundary, not from a demonstrated original-method impossibility.

## Artifact coverage

Coverage across the `40` common-core same-engine cases:

| artifact | coverage | notes |
|---|---:|---|
| `schema/ddl_mysql.sql` | `40/40` | present for every case |
| `schema/ddl_spark.sql` | `40/40` | present for every case |
| `validation/mysql_witness_data.sql` | `38/40` | missing only `PORT_0003`, `PORT_0005` |
| `validation/spark_witness_data.sql` | `38/40` | missing only `PORT_0003`, `PORT_0005` |

For the requested canary cases:

- `PERF_0006`: MySQL schema present, Spark schema present, MySQL witness present, Spark witness present
- `PERF_0007`: MySQL schema present, Spark schema present, MySQL witness present, Spark witness present
- `CONS_0005`: MySQL schema present, Spark schema present, MySQL witness present, Spark witness present

So the six requested canary rows are **not** blocked by missing schema or witness artifacts.

## Harness assumptions that are still PostgreSQL-only

The current recovered R-Bot generation harness and visible upstream runtime still contain PostgreSQL-only assumptions:

1. Engine gating in the existing generation runner:
   - the PG expansion runner is explicitly `pg_only`
   - non-PG rows are not routed through a generalized same-engine path
2. Upstream database adapter:
   - visible `my_rewriter/database.py` accepts only `db = postgresql`
   - non-PostgreSQL `DBArgs` construction raises `NotImplementedError`
3. Runner metadata and denominator labels:
   - current expansion runner is named and logged as `common_core_v0_40_pg40`
   - package notes, claim boundaries, and run results are PG-only
4. Engine-parameterized path selection:
   - schema and witness paths need to switch by engine
   - generated artifact labels and caveats need to keep MySQL/Spark explicit

## What needs to be parameterized by engine

- `engine` label in the row loop and metadata
- schema path selection:
  - MySQL: `schema/ddl_mysql.sql`
  - Spark: `schema/ddl_spark.sql`
- witness-data path selection:
  - MySQL: `validation/mysql_witness_data.sql`
  - Spark: `validation/spark_witness_data.sql`
- denominator and caveat text for the canary package
- upstream `DBArgs` / database-type handling
- any prompt or runner assumptions that name PostgreSQL specifically

## Why rows were previously unsupported

Current best classification for the earlier `80` MySQL/Spark unsupported rows:

- `not` proven method-scope exclusion
- `not` broad artifact absence
- `not` yet classified as genuine parser impossibility
- primarily:
  - unimplemented recovered harness route for non-PG same-engine generation
  - visible upstream PostgreSQL-only database adapter

## Risks expected before any human-run attempt

- dialect syntax mismatch
- function-semantic mismatch across engines
- PostgreSQL-only parser or adapter expectations in upstream code
- generated SQL extraction failures if engine-specific prompt outputs differ
- witness-data compatibility at later execution time

## Canary justification

A six-row generation canary is justified because:

- all six selected rows have the required schema and witness artifacts
- the cases already have retained PostgreSQL generation evidence, so they are good bounded probes
- the canary can distinguish:
  - package-preflight adapter failure
  - engine-route failure
  - row-level generation failure

## Safe conclusion

The right next step is a **bounded fail-closed canary package**, not a full `80`-row MySQL/Spark run.

Current status:

- MySQL/Spark support is **not** proven
- MySQL/Spark impossibility is **not** proven
- the immediate blocker is a recovered runtime/adapter limitation, especially the PostgreSQL-only `DBArgs` path

## Recommended next action

1. Create a six-row canary package for:
   - `PERF_0006:mysql`
   - `PERF_0006:spark`
   - `PERF_0007:mysql`
   - `PERF_0007:spark`
   - `CONS_0005:mysql`
   - `CONS_0005:spark`
2. Make the package fail closed at preflight if the non-PostgreSQL adapter is still not safely implemented.
3. Use the canary only as feasibility evidence, not as support evidence for a full MySQL/Spark result card.
