# LLM-R2 Supported PG3 PostgreSQL Execution/Checker Plan v1

This is planning only.

No PostgreSQL execution is authorized by this file.
No checker, timing, or speedup is authorized.
This packet does not create correctness, exact-match, timing, or `120`-row
evidence.

## Scope Recap

Current generated rows:

- `PERF_0006:pg`
- `PERF_0013:pg`
- `PERF_0024:pg`

Current upstream gate status:

- generation dry-run passed: `3 / 3`
- static SQL inspection passed: `3 / 3`
- PostgreSQL execution not run
- checker not run
- timing not run
- MySQL/Spark not run
- full `120` not run

## Input Artifact Table

| case_id | generated_sql_path | source_sql_path | ddl_pg_path | pg_witness_data_path |
| --- | --- | --- | --- | --- |
| `PERF_0006` | `runs/llm_r2_supported_pg3_generation_dry_run_01/retained_tmp_artifacts/PERF_0006/generated_sql_schema_native_clean_v1.sql` | `datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/1.sql` | `UNKNOWN_NOT_RECOVERED` | `UNKNOWN_NOT_RECOVERED` |
| `PERF_0013` | `runs/llm_r2_supported_pg3_generation_dry_run_01/retained_tmp_artifacts/PERF_0013/generated_sql_schema_native_clean_v1.sql` | `datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/5.sql` | `UNKNOWN_NOT_RECOVERED` | `UNKNOWN_NOT_RECOVERED` |
| `PERF_0024` | `runs/llm_r2_supported_pg3_generation_dry_run_01/retained_tmp_artifacts/PERF_0024/generated_sql_schema_native_clean_v2.sql` | `UNKNOWN_NOT_RECOVERED` | `UNKNOWN_NOT_RECOVERED` | `UNKNOWN_NOT_RECOVERED` |

## Future Execution/Checker Phases

### 1. Workspace Preparation

- Purpose:
  Freeze a dedicated human-run workspace layout for PG-only execution and
  checker staging.
- Required inputs:
  approved generated SQL paths, run directory, static SQL inspection packet,
  failure bucket policy.
- Expected outputs if future approved:
  workspace root, per-case staging directories, retained command log location,
  artifact retention manifest.
- Stop condition:
  workspace layout is not accepted or required staging destinations are missing.
- Failure bucket if failed:
  `unknown_not_recovered`
- Explicit non-claims:
  no PostgreSQL execution, checker, or timing occurs in this phase.

### 2. Source SQL Recovery

- Purpose:
  recover the exact source SQL artifact path for each PG3 case without guessing.
- Required inputs:
  retained prompt trace, retained staged query metadata, case-local source
  provenance if later supplied.
- Expected outputs if future approved:
  frozen source SQL paths or explicit unresolved-path note per case.
- Stop condition:
  source SQL path remains unrecovered for any case needed for checker planning.
- Failure bucket if failed:
  `unknown_not_recovered`
- Explicit non-claims:
  this phase does not run source SQL.

### 3. Generated SQL Staging

- Purpose:
  stage retained generated SQL into the approved PG-only execution workspace
  without modifying SQL text.
- Required inputs:
  retained generated SQL paths, approved workspace layout.
- Expected outputs if future approved:
  per-case staged candidate SQL files and staging manifest.
- Stop condition:
  staged candidate SQL cannot be copied or retained verbatim.
- Failure bucket if failed:
  `generation_failed`
- Explicit non-claims:
  generated SQL staging is not execution and is not correctness evidence.

### 4. PostgreSQL Execution

- Purpose:
  run source and candidate SQL under a separately approved human-run PG
  execution step.
- Required inputs:
  recovered source SQL, staged candidate SQL, recovered PG DDL path, recovered
  witness-data path, approved execution workspace.
- Expected outputs if future approved:
  source stdout/stderr, candidate stdout/stderr, exit codes, retained execution
  logs.
- Stop condition:
  PostgreSQL environment is unavailable, DDL/witness inputs are missing, or
  either query fails to execute cleanly.
- Failure bucket if failed:
  `execution_failed`
- Explicit non-claims:
  this phase is not authorized by this packet.

### 5. Output Capture

- Purpose:
  retain source/candidate outputs in a checker-ready shape.
- Required inputs:
  successful or partially successful PG execution outputs.
- Expected outputs if future approved:
  retained output files, artifact file list, command transcript, per-case run
  notes.
- Stop condition:
  output artifacts are incomplete or not reviewable.
- Failure bucket if failed:
  `unknown_not_recovered`
- Explicit non-claims:
  output capture alone is not exact-match evidence.

### 6. Exact-Match Checker

- Purpose:
  compare source and candidate outputs using the approved checker contract.
- Required inputs:
  retained source output, retained candidate output, recovered checker handoff
  paths, approved checker invocation plan.
- Expected outputs if future approved:
  checker output files and per-case checker status.
- Stop condition:
  checker inputs are incomplete or checker contract cannot be applied.
- Failure bucket if failed:
  `mismatch`
- Explicit non-claims:
  checker is not authorized by this packet.

### 7. Failure-Bucket Assignment

- Purpose:
  assign explicit fail-closed buckets after any future human-run PG execution
  and checker step.
- Required inputs:
  execution logs, checker outputs if any, failure bucket policy.
- Expected outputs if future approved:
  per-case bucket ledger with explicit denominator-visible outcomes.
- Stop condition:
  a case outcome cannot be assigned to an explicit bucket.
- Failure bucket if failed:
  `unknown_not_recovered`
- Explicit non-claims:
  bucket assignment is bookkeeping, not promotion.

### 8. Governance Review

- Purpose:
  review any future PG execution/checker packet before any broader planning.
- Required inputs:
  retained execution artifacts, retained checker artifacts, failure-bucket
  ledger, no-timing attestation.
- Expected outputs if future approved:
  governance review packet only.
- Stop condition:
  retained artifacts are incomplete or boundary claims exceed approved scope.
- Failure bucket if failed:
  `methodology_boundary`
- Explicit non-claims:
  governance review does not create result cards, proposed rows, or a
  leaderboard.

## Approval Requirements Before Execution

Future PG execution/checker human-run approval should require:

- generated SQL paths accepted
- source SQL paths recovered
- PostgreSQL DDL and witness-data paths recovered
- workspace layout accepted
- no timing planned
- no result card planned
- failure bucket policy accepted

## Explicit Non-Claims

- This is planning only.
- This does not authorize PostgreSQL execution.
- This does not authorize checker.
- This does not authorize timing or speedup.
- This does not claim correctness or exact match.
- This does not claim MySQL/Spark support.
- This does not claim full `120`-row evidence.
- This does not create a result card, proposed row, or leaderboard.
