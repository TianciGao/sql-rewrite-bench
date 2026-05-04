# CALCITE_HEP_REAL_ROUTE_CANARY_v0

## Status

This note records the first real-route Calcite HEP canary for:

- `python -m scripts.cli formal-calcite-hep-real-route-canary`
- `tools/calcite_hep/CalciteHepRewriteSmoke.java`
- `reports/formal_expansion/calcite_hep_real_route_canary_v0.json`

Scope is one canary only:

- `PERF_0006`

Explicit non-claim boundary:

- not PostgreSQL execution
- not checker-backed
- not speedup-scored
- not a claim that Calcite HEP baseline is implemented

## Commands Run

- `python -m py_compile scripts/cli.py`
- `python -m scripts.cli formal-calcite-hep-real-route-canary`
- `python -m scripts.cli formal-calcite-hep-real-route-canary --case-id PERF_0006 --execute`
- `python -m json.tool reports/formal_expansion/calcite_hep_real_route_canary_v0.json >/dev/null`

Implementation constraint used by the CLI:

- `GRADLE_USER_HOME=/tmp/calcite-gradle-home`

## Dry-Run Result

Dry-run outcome:

- status: success
- case id: `PERF_0006`
- route target: `calcite_hep_real_route_canary`
- planned only; no Java compile and no wrapper invocation

Interpretation:

- the canary CLI route is wired correctly
- the command points at case-local `source.sql` and `schema/ddl_pg.sql`
- the execute route remains generation-only and no-database

## Execute Result

Final execute outcome on `PERF_0006`:

- `Java wrapper compile status:` success
- `case id:` `PERF_0006`
- `parse status:` success
- `schema/ddl ingestion status:` success
- `validation status:` success
- `sql_to_rel status:` success
- `hep_planner status:` success
- `rel_to_sql status:` success
- `emitted SQL mode:` `calcite_rel_to_sql`
- `route_stage_reached:` `emit`
- `exact blocker:` none

This means the canary moved past original passthrough scaffold mode and reached a real Calcite route:

- schema-backed validation closed
- SQL-to-Rel conversion closed
- a bounded `HepPlanner` rule program ran
- SQL was emitted through Calcite `RelToSql`

## Output Characterization

Observed output path:

- `/tmp/calcite-hep-wrapper/real-route/perf_0006.sql`

Observed output characteristics:

- `candidate SQL emitted:` yes
- `emitted SQL is Calcite-generated or passthrough:` Calcite-generated
- `output matches frozen source under normalized comparison:` no
- `final semicolon normalization for parse:` yes

Representative effect:

- the emitted SQL rewrites `AVG(...)` expressions into `SUM(...) / COUNT(*)` form
- the emitted SQL adds Calcite-style quoting and `COALESCE(SUM(...), 0)` wrappers

That is sufficient evidence that this is no longer just parse smoke or passthrough emission.

## Exact Current State

- `Java wrapper compiled:` yes
- `wrapper executed:` yes
- `source.sql accepted:` yes
- `schema/ddl_pg.sql accepted:` yes
- `parse reached:` yes
- `validate reached:` yes
- `sql_to_rel reached:` yes
- `hep_planner reached:` yes
- `rel_to_sql reached:` yes
- `emit reached:` yes
- `emitted SQL mode:` `calcite_rel_to_sql`
- `whether emitted SQL is Calcite-generated:` yes
- `exact blocker if any:` none in the final canary execute result

## Interpretation

What this canary proves:

- the local Calcite checkout can support a real schema-backed planning route inside the repo wrapper
- `PERF_0006` can be parsed, validated, converted to rel, passed through a bounded HEP step, and emitted back to SQL without any database execution
- the wrapper can now distinguish real-route output from parse-only or passthrough fallback modes

What this still does not prove:

- no PostgreSQL execution closure exists
- no result-checker closure exists
- no speedup closure exists
- no broader multi-case Calcite HEP baseline exists yet
- no claim should be made that Calcite HEP is fully implemented as a benchmark baseline

## Next Step

Recommended next action:

- expand the real route to the clean 4-case PERF subset

Reason:

- schema ingestion, validation, rel conversion, bounded HEP, and rel-to-SQL all succeeded on the first canary
- the next incremental risk is subset generalization, not foundational planner closure

Only fall back to schema/validation/rel-conversion repair if one of the next cases breaks that route.

## Verification / Non-Modification Note

- no PostgreSQL workload was run
- no checker was run
- no speedup run was performed
- no registry file was modified
- no `docs/EXECUTION_STATUS.md` change was made
- no formal review file was modified
- no case file was modified
- no Gradle build outputs were added to git
