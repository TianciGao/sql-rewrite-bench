**Execution Plan**
This package prepares the broader non-PORT SQLGlot same-engine execution slice for Common-core v0. It expands beyond the 3-case canary to every non-PORT denominator case in `performance`, `consistency`, and `longtail`, while preserving generation-failed and explicit no-op rows instead of dropping them.

Scope:
- cases: `31` non-PORT denominator cases
- engines: `pg`, `mysql`, `spark`
- routes: `sqlglot_optimize_same_dialect`, `sqlglot_transpile_same_dialect_noop`
- total matrix rows: `186`
- ready-to-execute rows: `144`
- explicit generation-failed rows: `27`
- explicit no-op rows: `15`

Execution rules:
- run only rows with `execution_row_status=ready_to_execute`
- keep `not_executed_generation_failed` rows explicit in `run_results.json`
- keep `noop_generated` rows explicit in `run_results.json`
- do not execute any `PORT` case
- do not compute timing
- do not compute speedup or leaderboard metrics
- use the corrected runner logic from `sqlglot_same_engine_execution_canary_01`
- run from the real repository root with no `tmp_repo`

Runner reuse:
- `pg`: isolated schema-per-row execution via `psql`
- `mysql`: shared-database execution using `MYSQL_*` env vars plus per-row table cleanup before and after execution
- `spark`: per-row local warehouse isolation via workspace-local temporary warehouse directories

Expected ready rows by engine:
- `pg`: `48`
- `mysql`: `48`
- `spark`: `48`

Known method caveat:
- `CONS_0007 / sqlglot_optimize_same_dialect` should remain explicit if it fails on `pg`, `mysql`, and `spark`; the canary already established this as a SQLGlot-generated SQL issue around `e2.e1.commission`, not a runner failure.

