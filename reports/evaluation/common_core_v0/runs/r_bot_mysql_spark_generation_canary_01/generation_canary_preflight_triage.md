# R-Bot MySQL/Spark Generation Canary Preflight Triage

## Summary

This package produced **feasibility/preflight evidence only**.

- planned rows = `6`
- preflight_blocked rows = `6`
- generated rows = `0`
- failed rows = `0`
- unsupported rows = `0`

The package did **not** reach row-level generation. All six rows were stopped by the same package-level preflight blocker:

- `failure_category = engine_adapter_not_implemented_mysql_spark`
- `failure_reason = Visible upstream my_rewriter/database.py still only implements db=postgresql`

## Planned rows

- `PERF_0006:mysql`
- `PERF_0006:spark`
- `PERF_0007:mysql`
- `PERF_0007:spark`
- `CONS_0005:mysql`
- `CONS_0005:spark`

## What this result means

This is **not** evidence of MySQL or Spark generation failure yet.

The canary failed earlier than row generation because the visible upstream runtime still exposes a PostgreSQL-only database adapter path. In the retained canary runner, the preflight check inspects `my_rewriter/database.py` and blocks the package when that file still only implements `db=postgresql` and otherwise raises `NotImplementedError`.

## What this result does not mean

This is **not**:

- artifact absence
- provider auth failure
- row-level MySQL generation failure
- row-level Spark generation failure
- execution evidence
- timing evidence

## Why this is not artifact absence

The retained feasibility audit already established:

- `ddl_mysql.sql`: `40/40` present
- `ddl_spark.sql`: `40/40` present
- `mysql_witness_data.sql`: `38/40` present
- `spark_witness_data.sql`: `38/40` present

For the six selected canary rows specifically:

- schema files are present for both MySQL and Spark
- witness-data files are present for both MySQL and Spark

So the preflight block is not caused by missing case assets.

## Why this is not provider auth failure

The canary runner has a separate optional provider preflight behind:

- `RBOT_CANARY_ALLOW_PROVIDER_PREFLIGHT_CALL=1`

The retained `run_results.json` records:

- `failure_category = engine_adapter_not_implemented_mysql_spark`

not a provider-auth category. So this stop happened before any optional provider auth probe was the deciding blocker.

## Recommended next step

A bounded non-PG generation adapter recovery patch is justified.

That patch should target the recovered upstream/runtime adapter layer, not the benchmark cases. The next recovery step should be narrowly scoped to making the non-PostgreSQL generation route safe enough for a later six-row canary rerun.

## Boundary

This triage is:

- feasibility/preflight evidence only

It is **not**:

- generation evidence
- execution/validity evidence
- timing evidence
- speedup evidence
- leaderboard evidence
