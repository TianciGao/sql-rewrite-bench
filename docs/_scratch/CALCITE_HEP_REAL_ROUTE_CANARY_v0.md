# CALCITE_HEP_REAL_ROUTE_CANARY_v0

## Status

This note records the expanded 4-case Calcite HEP real-route canary for:

- `python -m scripts.cli formal-calcite-hep-real-route-canary`
- `tools/calcite_hep/CalciteHepRewriteSmoke.java`
- `reports/formal_expansion/calcite_hep_real_route_canary_v0.json`

Scope is the clean 4-case PERF subset:

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

Explicit non-claim boundary:

- no PostgreSQL execution
- no checker
- no speedup
- not final Calcite HEP baseline
- not a claim that Calcite HEP is fully implemented as a benchmark baseline

## Commands Run

- `python -m py_compile scripts/cli.py`
- `python -m scripts.cli formal-calcite-hep-real-route-canary`
- `python -m scripts.cli formal-calcite-hep-real-route-canary --case-id PERF_0006 --case-id PERF_0008 --case-id PERF_0033 --case-id PERF_0054 --execute`
- `python -m json.tool reports/formal_expansion/calcite_hep_real_route_canary_v0.json >/dev/null`

Implementation constraint used by the CLI:

- `GRADLE_USER_HOME=/tmp/calcite-gradle-home`

## Dry-Run Result

Dry-run outcome:

- status: success
- denominator surfaced: `4`
- selected cases:
  - `PERF_0006`
  - `PERF_0008`
  - `PERF_0033`
  - `PERF_0054`
- route target: `calcite_hep_real_route_canary`
- dry-run only; no Java compile and no wrapper invocation

Interpretation:

- the real-route CLI is wired for the intended 4-case subset
- the command resolves case-local `source.sql` and `schema/ddl_pg.sql` for all four cases
- the route remains generation-only and no-database

## 4-Case Execute Result

Final real-route outcome on the clean 4-case PERF subset:

- `Java wrapper compile status:` success
- `real-route success count:` `4/4`
- `parse success count:` `4/4`
- `validation success count:` `4/4`
- `sql_to_rel success count:` `4/4`
- `HepPlanner success count:` `4/4`
- `RelToSql success count:` `4/4`
- `emit success count:` `4/4`
- `emitted SQL mode distribution:` `calcite_rel_to_sql=4`

Per-case result:

| case_id | source accepted | DDL accepted | parse | DDL ingestion | validate | sql_to_rel | HepPlanner | rel_to_sql | emit | emitted SQL mode | Calcite-generated | normalized output differs from source | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | yes | yes | yes | yes | yes | yes | yes | yes | yes | `calcite_rel_to_sql` | yes | yes | none |
| `PERF_0008` | yes | yes | yes | yes | yes | yes | yes | yes | yes | `calcite_rel_to_sql` | yes | yes | none |
| `PERF_0033` | yes | yes | yes | yes | yes | yes | yes | yes | yes | `calcite_rel_to_sql` | yes | yes | none |
| `PERF_0054` | yes | yes | yes | yes | yes | yes | yes | yes | yes | `calcite_rel_to_sql` | yes | yes | none |

Observed parse kind for all four cases:

- `ORDER_BY`

## What Closed

All four cases now close the same generation-only real route:

1. parse
2. schema / DDL ingestion
3. validation
4. SQL-to-Rel conversion
5. bounded `HepPlanner`
6. `RelToSql`
7. emit

This required widening the tiny local DDL bridge to handle:

- multi-table `ddl_pg.sql` files
- table-level `PRIMARY KEY (...)`
- inline `PRIMARY KEY`
- `char(n)`, `varchar(n)`, `numeric(p,s)`, and `text`
- balanced-parenthesis parsing rather than regex-shortcut matching

## Output Characterization

Observed output characteristics across the subset:

- all emitted SQL is Calcite-generated
- all four outputs differ from the frozen source under normalized comparison
- none of the four cases used passthrough fallback
- none of the four cases stopped at `calcite_parse_only`

Representative effect:

- Calcite rewrites `AVG(...)` into `SUM(...) / COUNT(*)` style expressions where applicable
- emitted SQL uses Calcite/PostgreSQL dialect rendering and explicit quoting

## Interpretation

What this result proves:

- the local Calcite checkout can support a schema-backed planning route on the clean 4-case PERF subset
- the wrapper now reaches real planner stages, not just parse smoke
- the subset has generation-only closure through `RelToSql`

What this still does not prove:

- no PostgreSQL execution closure exists yet
- no result-checker closure exists yet
- no speedup closure exists yet
- no final benchmark baseline claim should be made from this result alone

## Blockers

Final 4-case execute blockers:

- none

Intermediate engineering blockers that were fixed before the final run:

- single-table-only DDL parsing
- unsupported `PRIMARY KEY` lines
- unsupported `text`
- regex-based `CREATE TABLE` matching that broke on `char(n)` / `varchar(n)`

## Next Action

Because the 4-case real-route succeeds `4/4`, the next step should be:

- run Calcite HEP PG execution/checker preflight

That is the correct next boundary because generation-only real-route closure now exists on the clean subset.

## Verification / Non-Modification Note

- no PostgreSQL workload was run
- no checker was run
- no speedup run was performed
- no registry file was modified
- no `docs/EXECUTION_STATUS.md` change was made
- no formal review file was modified
- no case file was modified
- no Gradle build outputs were added to git
