# CALCITE_HEP_PG_CHECKER_PREFLIGHT_v0

## Status

This note records PostgreSQL execution/checker preflight only for the Calcite HEP real-route 4-case PERF subset:

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

Explicit non-claim boundary:

- preflight only
- no PostgreSQL execution
- no checker
- no speedup
- not final Calcite HEP baseline
- not a claim that Calcite HEP is fully implemented

## Commands Run

- `python -m py_compile scripts/cli.py`
- `python -m scripts.cli formal-calcite-hep-pg-checker-preflight`
- `python -m json.tool reports/formal_expansion/calcite_hep_pg_checker_preflight_v0.json >/dev/null`
- `python -m scripts.cli formal-calcite-hep-pg-checker-preflight --execute || true`
- `python -m json.tool reports/formal_expansion/calcite_hep_pg_checker_preflight_execute_refused_v0.json >/dev/null`

## 4-Case Readiness Result

Final preflight result:

- `ready_count:` `4/4`
- `blocked_count:` `0/4`
- `ready_cases:` `PERF_0006`, `PERF_0008`, `PERF_0033`, `PERF_0054`
- `blocked_cases:` none
- `generated_sql_recoverable_count:` `4/4`
- `calcite_rel_to_sql_count:` `4/4`
- `passthrough_fallback_count:` `0/4`
- `PG execution/checker can proceed:` yes, at the preflight level

Per-case closure:

| case_id | source.sql | ddl_pg.sql | validation schema expected | Calcite-generated SQL recoverable | emitted_sql_mode | passthrough | source PG evidence | checker path plannable | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | yes | yes | `perf_0006_validation` | yes | `calcite_rel_to_sql` | no | yes | yes | none |
| `PERF_0008` | yes | yes | `perf_0008_validation` | yes | `calcite_rel_to_sql` | no | yes | yes | none |
| `PERF_0033` | yes | yes | `perf_0033_validation` | yes | `calcite_rel_to_sql` | no | yes | yes | none |
| `PERF_0054` | yes | yes | `perf_0054_validation` | yes | `calcite_rel_to_sql` | no | yes | yes | none |

What was verified for all four cases:

- `source.sql` exists
- `schema/ddl_pg.sql` exists
- the real-route report record exists
- `emitted_sql_mode=calcite_rel_to_sql`
- output is marked Calcite-generated, not passthrough
- emitted SQL is still recoverable from `/tmp/calcite-hep-wrapper/real-route/*.sql`
- PostgreSQL source witness evidence exists at `cases/PERF/.../runs/pg/source.tsv`
- PostgreSQL source result-check evidence exists at `cases/PERF/.../runs/pg/result_check.json`
- case-local `validation/checker.yaml` exists
- source/candidate TSV materialization paths and checker JSON paths can be planned without execution

## Planned Handoff Paths

Planned source TSV materialization paths:

- `reports/formal_expansion/result_materialization/calcite_hep/source/perf_0006.tsv`
- `reports/formal_expansion/result_materialization/calcite_hep/source/perf_0008.tsv`
- `reports/formal_expansion/result_materialization/calcite_hep/source/perf_0033.tsv`
- `reports/formal_expansion/result_materialization/calcite_hep/source/perf_0054.tsv`

Planned candidate TSV materialization paths:

- `reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0006.tsv`
- `reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0008.tsv`
- `reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0033.tsv`
- `reports/formal_expansion/result_materialization/calcite_hep/calcite_rel_to_sql/perf_0054.tsv`

Planned checker JSON paths:

- `reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0006.json`
- `reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0008.json`
- `reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0033.json`
- `reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/perf_0054.json`

Planned policy boundary:

- execute source and Calcite candidate SQL on PostgreSQL in a later step
- reuse case-local `validation/checker.yaml` semantics after candidate materialization
- keep speedup disabled at this stage

## Execute Refusal

`--execute` is intentionally refused for this command.

- refusal artifact: `reports/formal_expansion/calcite_hep_pg_checker_preflight_execute_refused_v0.json`
- refusal reason: this is a preflight-only command and must not run PostgreSQL execution or checker work

## Blockers

Final blockers:

- none

## Interpretation

What this proves:

- the 4-case real-route subset is wired strongly enough to hand off into a future PostgreSQL execution/checker step
- Calcite-generated SQL is recoverable for all four cases
- existing PostgreSQL source witness evidence and checker policy artifacts are already present case-locally

What this does not prove:

- no PostgreSQL execution closure has been demonstrated for Calcite candidates
- no checker closure has been demonstrated for Calcite candidates
- no speedup or leaderboard claim is justified

## Next Action

Because preflight is ready `4/4`, the next step can be:

- run Calcite HEP PG execution/checker on the 4-case subset

That next step should stay explicit about boundary:

- execution and checker only
- still no speedup until checker-backed execution artifacts exist
