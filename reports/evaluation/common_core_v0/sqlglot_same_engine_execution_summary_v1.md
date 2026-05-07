**SQLGlot Same-Engine Execution Summary v1**

This combines the two denominator-aware SQLGlot same-engine execution evidence packages:

- `sqlglot_same_engine_nonport_execution_01`
- `sqlglot_same_engine_port_execution_resolved_01`

This is execution evidence only. It is not a timing package, not a speedup package, and not a final same-engine leaderboard.

**Coverage**
- total cases = `40`
- total planned SQLGlot same-engine rows = `240`
- non-PORT rows = `186`
- PORT rows = `54`

**Counts By Status**
- `success`: `137`
- `failure`: `16`
- `skipped`: `87`

Interpretation:
- `137` rows have executed success evidence
- `16` rows have executed failure evidence
- `87` rows remain explicit non-executed rows rather than being dropped

**Counts By Route**
- `sqlglot_optimize_same_dialect`: `120`
- `sqlglot_transpile_same_dialect_noop`: `120`

**Counts By Engine**
- `pg`: `80`
- `mysql`: `80`
- `spark`: `80`

**Counts By Pool**
- `performance`: `96`
- `consistency`: `54`
- `longtail`: `36`
- `portability`: `54`

**Explicit Non-Execution Buckets**
- `generation_failed`: `27`
- `noop_generated`: `24`
- `skipped_unsupported`: `36`

These rows remain explicit in the evidence and were not silently removed from denominator accounting.

**Source Package Validator Status**
- `sqlglot_same_engine_nonport_execution_01`: `ok=true`, `issue_count=0`
- `sqlglot_same_engine_port_execution_resolved_01`: `ok=true`, `issue_count=0`

**PORT Note**
- The earlier `PORT_0003` and `PORT_0005` PostgreSQL optimize failures were package witness gaps, not SQLGlot method failures.
- Those gaps were resolved by the targeted `pg_witness_data.sql` backfill and retry package.
- They are therefore not counted here as SQLGlot method failures.

**Readiness Boundary**
- This summary supports denominator-aware SQLGlot same-engine execution evidence reporting.
- It does not support timing analysis.
- It does not support `GM_Speedup`, regression-rate, or final same-engine leaderboard claims.
- Speedup metrics remain `not ready`.

No `same_engine_leaderboard.csv` has been created in this step.
