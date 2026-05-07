# Controls v0 Manual Spark Backfill PERF4 01

This package is for a human to run from the real repository root. Codex must not execute the script as part of this package creation step.

Scope:
- cases: `PERF_0006`, `PERF_0007`, `PERF_0008`, `PERF_0013`
- engine: `spark`
- validation only
- no `pg` or `mysql` execution here
- no plan collection yet
- no separate hard-negative command

Purpose:
- backfill fresh Spark validation entrypoints for the four Common-core v0 performance cases that previously had only legacy Spark artifacts

What success means:
- the new Spark validation scripts for these four cases can run from the real repo root
- stdout/stderr logs and `run_results.json` are produced under this run directory

Follow-on expectation:
- these four cases can then move from Spark `artifact_reuse_only` toward fresh Spark execution coverage
- `run_event_long` materialization comes only after this manual backfill succeeds and the human confirms the refreshed case-local artifacts are trustworthy

Warning:
- case-local Spark artifacts under `cases/PERF/<case>/runs/spark/` may be regenerated
- the script does not `git add` anything
