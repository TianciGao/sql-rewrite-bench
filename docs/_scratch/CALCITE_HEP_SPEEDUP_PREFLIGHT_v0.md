# CALCITE_HEP_SPEEDUP_PREFLIGHT_v0

## Status

This note records speedup preflight only for the bounded 4-case Calcite HEP checker-backed PERF subset:

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0054`

Explicit boundary:

- preflight only
- no speedup
- no PostgreSQL runtime benchmark
- not final Calcite HEP baseline
- not a claim that Calcite HEP is fully implemented

## Commands Run

1. `python -m py_compile scripts/cli.py`
2. `python -m scripts.cli formal-calcite-hep-speedup-preflight`
3. `python -m json.tool reports/formal_expansion/calcite_hep_speedup_preflight_v0.json >/dev/null`
4. `python -m scripts.cli formal-calcite-hep-speedup-preflight --execute || true`
5. `python -m json.tool reports/formal_expansion/calcite_hep_speedup_preflight_execute_refused_v0.json >/dev/null`

## 4-Case Readiness Result

Final preflight result:

- `case_count:` `4`
- `ready_count:` `4/4`
- `blocked_count:` `0/4`
- `ready_cases:` `PERF_0006`, `PERF_0008`, `PERF_0033`, `PERF_0054`
- `blocked_cases:` none
- `checker_consistent_count:` `4/4`
- `candidate_sql_recoverable_count:` `4/4`
- `calcite_rel_to_sql_count:` `4/4`
- `speedup run can proceed:` yes, at the preflight level

Per-case readiness:

| case_id | real-route record | emitted_sql_mode | candidate SQL recoverable | checker JSON | checker status | row-count equal | validation schema | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PERF_0006` | yes | `calcite_rel_to_sql` | yes | yes | `consistent` | yes | `perf_0006_validation` | none |
| `PERF_0008` | yes | `calcite_rel_to_sql` | yes | yes | `consistent` | yes | `perf_0008_validation` | none |
| `PERF_0033` | yes | `calcite_rel_to_sql` | yes | yes | `consistent` | yes | `perf_0033_validation` | none |
| `PERF_0054` | yes | `calcite_rel_to_sql` | yes | yes | `consistent` | yes | `perf_0054_validation` | none |

What was verified for all four cases:

- real-route record exists in `reports/formal_expansion/calcite_hep_real_route_canary_v0.json`
- `emitted_sql_mode=calcite_rel_to_sql`
- candidate SQL is still recoverable from `/tmp/calcite-hep-wrapper/real-route/*.sql`
- source SQL path exists
- expected PostgreSQL validation schema name is available
- checker JSON exists under `reports/formal_expansion/result_checks/calcite_hep/calcite_rel_to_sql/*.json`
- `checker_status=consistent`
- source and candidate row counts are equal
- runtime policy is defined for a future bounded speedup run

## Runtime Policy

Recorded runtime policy for a future speedup run:

- `warmup_count=1`
- `repeat_count=5`
- `statement_timeout_ms=30000`
- `primary_statistic=median`
- `tie_threshold=0.05`
- `regression_threshold=1.2`

Planned speedup output path:

- `reports/formal_expansion/calcite_hep_speedup_run_v0.json`

## Execute Refusal

`--execute` is intentionally refused for this command.

- refusal artifact: `reports/formal_expansion/calcite_hep_speedup_preflight_execute_refused_v0.json`
- refusal reason: this command is preflight-only and must not run runtime repeats or speedup scoring

## Blockers

Final blockers:

- none

## Interpretation

What this proves:

- the bounded 4-case Calcite HEP subset is now speedup-ready at the artifact-preflight level
- all four cases are checker-backed and have recoverable Calcite-generated SQL
- the runtime policy boundary for a later speedup step is now recorded explicitly

What this does not prove:

- no PostgreSQL runtime benchmark has been executed here
- no speedup scoring result exists yet
- no final Calcite HEP baseline claim is justified

## Next Action

Because the bounded subset is ready `4/4`, the next step can be:

- run the bounded 4-case Calcite HEP speedup run

That next step should stay explicit about boundary:

- PostgreSQL-only
- speedup-scored only after runtime repeats complete
- still not a final Calcite HEP baseline claim
