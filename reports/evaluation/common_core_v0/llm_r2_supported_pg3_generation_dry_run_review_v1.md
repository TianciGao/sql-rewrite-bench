# LLM-R2 Supported PG3 Generation Dry-run Governance Review v1

This is governance review of a completed local human-run generation dry-run.

This is not paper evidence yet.
This is not PostgreSQL execution evidence.
This is not checker evidence.
This is not timing or speedup evidence.
This is not MySQL or Spark evidence.
This is not full `120` evidence.

## Scope Recap

Approved rows:

- `PERF_0006:pg`
- `PERF_0013:pg`
- `PERF_0024:pg`

Approved scope:

- LLM-R2 runner invocation
- output SQL extraction
- generated SQL retention
- failure-bucket assignment

Not approved and not run:

- PostgreSQL execution
- checker
- timing
- speedup
- MySQL/Spark
- full `120` generation
- result card / proposed row

## Per-Row Result Table

| case_id | engine | generation_attempted | runner_invoked | exit_code | raw_output_retained | output_sql_extracted | generated_sql_retained | failure_bucket |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| `PERF_0006` | `pg` | `true` | `true` | `0` | `true` | `true` | `true` | `generated` |
| `PERF_0013` | `pg` | `true` | `true` | `0` | `true` | `true` | `true` | `generated` |
| `PERF_0024` | `pg` | `true` | `true` | `0` | `true` | `true` | `true` | `generated` |

## Retained Artifact Table

| case_id | generated_sql_path | raw_output_paths | stdout_path | stderr_path | runtime_snapshot_path |
| --- | --- | --- | --- | --- | --- |
| `PERF_0006` | `retained_tmp_artifacts/PERF_0006/generated_sql_schema_native_clean_v1.sql` | result CSV, prompt trace, demo trace, activated rules JSON | `logs/PERF_0006.stdout.log` | `logs/PERF_0006.stderr.log` | `runtime_snapshots/PERF_0006_files.txt` |
| `PERF_0013` | `retained_tmp_artifacts/PERF_0013/generated_sql_schema_native_clean_v1.sql` | result CSV, prompt trace, demo trace, activated rules JSON | `logs/PERF_0013.stdout.log` | `logs/PERF_0013.stderr.log` | `runtime_snapshots/PERF_0013_files.txt` |
| `PERF_0024` | `retained_tmp_artifacts/PERF_0024/generated_sql_schema_native_clean_v2.sql` | result CSV, prompt trace, demo trace, activated rules JSON | `logs/PERF_0024.stdout.log` | `logs/PERF_0024.stderr.log` | `runtime_snapshots/PERF_0024_files.txt` |

## Generated SQL Retention Summary

Generated SQL retention is present for all 3 rows.

- `PERF_0006`
  - retained generated SQL present
  - retained clean extracted SQL present
- `PERF_0013`
  - retained generated SQL present
  - retained clean extracted SQL present
- `PERF_0024`
  - retained generated SQL present
  - retained clean extracted SQL present
  - an additional clean `v1` artifact is also retained, while the generation
    ledger points to clean `v2`

## No-DB / Checker / Timing Attestation Summary

The retained attestation confirms:

- PostgreSQL execution not run
- checker not run
- timing not run
- speedup not run
- MySQL/Spark not run
- full `120` generation not run

## Gate Decision

The retained run passes the **generation dry-run gate** for the supported PG3
subset.

Reason:

- all 3 approved rows were attempted
- all 3 rows show runner invocation
- all 3 rows exited with code `0`
- all 3 rows retained raw outputs
- all 3 rows retained extracted output SQL
- all 3 rows retained generated SQL
- all 3 rows received explicit `generated` failure-bucket accounting
- a separate no-DB/checker/timing attestation is retained

## Next Recommended Gate

Review retained LLM-R2 PG3 generated SQL and decide whether to authorize
**static SQL inspection only** before any later execution discussion.

## Explicit Non-Claims

- This review does not create paper evidence.
- This review does not create a result card or proposed row.
- This review does not authorize PostgreSQL execution.
- This review does not authorize checker, timing, or speedup.
- This review does not claim MySQL/Spark support.
- This review does not claim full `120`-row evidence.
