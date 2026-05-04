# CALCITE_HEP_PERF0006_NUMERIC_FIX_v0

## Status

This note records the targeted `PERF_0006` AVG precision fix for the Calcite HEP real-route wrapper and the bounded rerun of the `PERF_0006` checker canary.

Boundary:

- diagnostic/fix only
- no speedup
- no final baseline claim
- not a claim that Calcite HEP is fully implemented

## Code-Level Fix

File changed:

- `tools/calcite_hep/CalciteHepRewriteSmoke.java`

Exact fix:

- added a `REDUCED_AVG_PATTERN` regex that matches Calcite’s emitted
  `CAST(CAST(COALESCE(SUM(...), 0) AS DECIMAL(15, 2)) / COUNT(*) AS DECIMAL(15, 2))`
  aggregate-reduction shape
- added `restoreAvgPrecision(...)`
- applied that post-processing step immediately after `RelToSql`

Resulting behavior:

- real-route emission still stays `calcite_rel_to_sql`
- no passthrough fallback was introduced
- AVG-derived columns are emitted back as `AVG(...)` instead of the lossy `DECIMAL(15,2)` reduced form

## Emitted SQL Before / After

Affected AVG columns before the fix:

- `avg_qty`: `CAST(CAST(COALESCE(SUM("l_quantity"), 0) AS DECIMAL(15, 2)) / COUNT(*) AS DECIMAL(15, 2))`
- `avg_price`: `CAST(CAST(COALESCE(SUM("l_extendedprice"), 0) AS DECIMAL(15, 2)) / COUNT(*) AS DECIMAL(15, 2))`
- `avg_disc`: `CAST(CAST(COALESCE(SUM("l_discount"), 0) AS DECIMAL(15, 2)) / COUNT(*) AS DECIMAL(15, 2))`

Affected AVG columns after the fix:

- `avg_qty`: `AVG("l_quantity")`
- `avg_price`: `AVG("l_extendedprice")`
- `avg_disc`: `AVG("l_discount")`

Why this fix was needed:

- the reduced form rounded `avg_disc` from source `0.075` to Calcite `0.08`
- exact TSV checker therefore failed even though row counts matched

## PERF_0006 Checker Result

Commands run:

1. `python -m py_compile scripts/cli.py`
2. `python -m scripts.cli formal-calcite-hep-real-route-canary --case-id PERF_0006 --execute`
3. `python -m json.tool reports/formal_expansion/calcite_hep_real_route_canary_v0.json >/dev/null`
4. `export PGPASSWORD='123456'`
5. `source scripts/env_postgres.sh`
6. `python -m scripts.cli formal-calcite-hep-pg-checker-run --case-id PERF_0006 --execute`
7. `python -m json.tool reports/formal_expansion/calcite_hep_pg_checker_run_v0.json >/dev/null`
8. `python -m json.tool reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0006.json >/dev/null`

Bounded canary outcome:

- emitted SQL mode: `calcite_rel_to_sql`
- source PG execution: success
- candidate PG execution: success
- source row count: `2`
- candidate row count: `2`
- row-count match: yes
- exact TSV byte equality: yes
- checker status: `consistent`

Interpretation:

- the `PERF_0006` AVG precision mismatch is fixed
- the previous `avg_disc` rounding failure is no longer present

## Recovery Status

Did 4-case checker-clean recovery succeed?

- not yet fully reverified in this step

What did succeed:

- the only previously failing canary case, `PERF_0006`, is now checker-consistent

What follows from that:

- a bounded full 4-case PostgreSQL checker rerun is now appropriate

## Fallback Recommendation

Fallback to the 3-case checker-clean subset is no longer the preferred next action.

Preferred next action now:

- rerun the bounded 4-case PostgreSQL checker subset

Use the 3-case subset fallback only if:

- a fresh 4-case rerun exposes a new inconsistency after this fix

## Conclusion

The fix was a targeted post-`RelToSql` AVG-precision restoration in the Calcite wrapper. It preserves real-route Calcite generation while removing the `DECIMAL(15,2)` AVG cast loss that broke `PERF_0006`. The repaired `PERF_0006` canary is now exact-TSV consistent, so a full 4-case checker-clean recovery rerun is the correct next bounded step.
