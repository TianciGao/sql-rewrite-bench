**SQLGlot Validity Summary v1**

This is a validity/execution-only summary built from the completed SQLGlot same-engine execution evidence packages for Common-core v0.

It is not a timing package, not a speedup package, and not a performance leaderboard.

**Overall**
- planned rows: `240`
- executed rows: `153`
- executable success count: `137`
- executable failure count: `16`
- executable_rate over full planned denominator: `0.5708`
- executable_rate over executable-attempt denominator: `0.8954`
- generation_failed count: `27` rate=`0.1125`
- noop_generated count: `24` rate=`0.1000`
- skipped_unsupported count: `36` rate=`0.1500`

**By Route**
- `sqlglot_optimize_same_dialect`: planned=`120`, executed=`75`, success=`65`, failure=`10`, exec_rate_planned=`0.5417`, exec_rate_attempted=`0.8667`, generation_failed=`27`, noop_generated=`0`, skipped_unsupported=`18`
- `sqlglot_transpile_same_dialect_noop`: planned=`120`, executed=`78`, success=`72`, failure=`6`, exec_rate_planned=`0.6000`, exec_rate_attempted=`0.9231`, generation_failed=`0`, noop_generated=`24`, skipped_unsupported=`18`

**Failure Buckets**
- `method_error`: `36`
- `parse_error`: `7`
- `unsupported`: `60`

**Counts By Pool**
- `consistency`: `54`
- `longtail`: `36`
- `performance`: `96`
- `portability`: `54`

**Counts By Engine**
- `mysql`: `80`
- `pg`: `80`
- `spark`: `80`

**Counts By Route**
- `sqlglot_optimize_same_dialect`: `120`
- `sqlglot_transpile_same_dialect_noop`: `120`

**Boundary**
- This package reports validity/execution-only evidence.
- It does not report timing.
- It does not report speedup.
- It does not create a performance leaderboard.
- Performance metrics remain `not ready`.

**PORT Note**
- The earlier PORT witness gaps for `PORT_0003` and `PORT_0005` PostgreSQL optimize rows were resolved by targeted `pg_witness_data.sql` backfill and retry.
- Those package gaps are therefore not counted as SQLGlot method failures in this validity summary.
