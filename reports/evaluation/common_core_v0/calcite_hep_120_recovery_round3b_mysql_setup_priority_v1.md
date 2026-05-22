# Calcite HEP 120 Recovery Round-3b MySQL Setup Priority v1

This audit is limited to the two MySQL rows that failed in
`calcite_hep_120_recovery_round3_canary_10_01` before exact-match comparison:

- `PERF_0062:mysql`
- `LONGTAIL_0013:mysql`

## Retained Failure Cause

Both rows failed on the first MySQL setup command issued by the Round-3 runner:

- `DROP DATABASE IF EXISTS ccv0_calcite_hep_r3_perf_0062_mysql`
- `DROP DATABASE IF EXISTS ccv0_calcite_hep_r3_longtail_0013_mysql`

Retained stderr for both rows shows:

- `ERROR 1044 (42000): Access denied for user 'bench'@'127.0.0.1' to database ...`

Interpretation:

- the failure occurred before schema load, witness load, source execution, or
  generated-query execution
- this is a MySQL setup / privilege isolation defect in the Round-3 harness
  strategy
- it is not retained evidence of method correctness failure
- it is not retained evidence of exact-output mismatch for the Round-3 rendered
  SQL on these two rows

## Round-3b Decision

A bounded Round-3b canary is justified.

Safe package change:

- do not retry the full Round-3 canary
- do not touch PostgreSQL or Spark rows
- do not change the checker
- do not create or drop per-row databases
- reuse the existing `MYSQL_DATABASE` from `scripts/env_mysql.sh`
- use per-row table cleanup inside that existing database before and after each
  row
- reuse the retained Round-3 generated SQL for these two rows

## Expected Ledger Outcomes

- `0` recovered => ledger remains `84/120`
- `1` recovered => ledger becomes `85/120`
- `2` recovered => ledger becomes `86/120`

## Paper-Safe Interpretation

If Round-3b later succeeds, it should be described as setup-harness recovery
only. A row still counts as recovered only if the retained Round-3 generated
MySQL SQL executes and matches exactly under the unchanged checker.

If Round-3b later fails, that strengthens the conclusion that at least one or
both rows remain non-exact for reasons beyond the per-row temporary database
strategy.
