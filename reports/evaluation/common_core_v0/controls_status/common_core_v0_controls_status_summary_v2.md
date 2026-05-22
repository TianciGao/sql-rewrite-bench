# Common-core v0 Controls Status Summary v2

This table combines:
- PG/MySQL controls from `controls_v0_manual_pg_mysql_40_01`
- Spark ready-subset controls from `controls_v0_manual_spark_ready36_resolved_01`
- Spark PERF backfill controls from `controls_v0_manual_spark_backfill_perf4_01`

## Total Rows

- total expected rows: `40 x 3 engines x 3 routes = 360`
- total materialized rows: `360`

## Counts By Evidence Mode

- `fresh_manual_validation`: `324`
- `artifact_reuse_only`: `0`
- `skipped_unsupported`: `36`
- `missing`: `0`

## Counts By Status

- `success`: `324`
- `skipped`: `36`
- `failed`: `0`
- `artifact_reuse_available`: `0`
- `missing`: `0`

## Counts By Engine

- `pg`: `120`
- `mysql`: `120`
- `spark`: `120`

## Fresh Coverage Summary

- fresh manual validation rows: `324`
- artifact reuse only rows: `0`
- skipped unsupported rows: `36`
- missing rows: `0`

## Status Statement

Controls are now denominator-complete with fresh PG/MySQL/Spark validation evidence, except explicitly unsupported PORT route-engine combinations.

The four previously artifact-reuse-only Spark PERF cases are now covered by fresh manual Spark validation backfill:
- `PERF_0006`
- `PERF_0007`
- `PERF_0008`
- `PERF_0013`
