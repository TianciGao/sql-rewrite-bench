# PORT_CROSS_ENGINE_BOUNDED_EXECUTION_v0

## Scope

- Approved subset only:
  - `PORT_0022`
  - `PORT_0024`
  - `PORT_0025`
- Engines:
  - `mysql`
  - `spark`
- Boundary:
  - bounded `3`-case MySQL + Spark execution only
  - no PostgreSQL
  - no SQLGlot
  - no model calls
  - no registry writeback
  - not full PORT closure

## Aggregate Result

- `case_count=3`
- `engine_count=2`
- `mysql_execution_success_count=1`
- `mysql_consistency_success_count=1`
- `spark_execution_success_count=1`
- `spark_consistency_success_count=1`
- `both_engine_execution_success_count=1`
- `both_engine_consistency_success_count=1`
- `failures_by_engine`:
  - `mysql=2`
  - `spark=2`
- `failures_by_category`:
  - `rewrite_execution_failed=2`
  - `source_execution_failed=2`

Claim boundary:

- `bounded_3_case_mysql_spark_execution_not_full_port_closure`

## Per-Case / Per-Engine Summary

| case_id | engine | schema load | witness load | source | rewrite_pos_01 | checker | consistency | row_count_source | row_count_rewrite | normalization policy | failure category |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PORT_0022` | `mysql` | success | success | success | failed | not_checked | not_checked | `1` | n/a | `normalized_tsv_report_local` | `rewrite_execution_failed` |
| `PORT_0022` | `spark` | success | success | failed | not_attempted | not_checked | not_checked | n/a | n/a | `normalized_tsv_report_local` | `source_execution_failed` |
| `PORT_0024` | `mysql` | success | success | success | success | consistent | consistent | `1` | `1` | `normalized_tsv_report_local` | `none` |
| `PORT_0024` | `spark` | success | success | success | success | consistent | consistent | `1` | `1` | `normalized_tsv_report_local` | `none` |
| `PORT_0025` | `mysql` | success | success | success | failed | not_checked | not_checked | `1` | n/a | `exact_tsv_report_local` | `rewrite_execution_failed` |
| `PORT_0025` | `spark` | success | success | failed | not_attempted | not_checked | not_checked | n/a | n/a | `exact_tsv_report_local` | `source_execution_failed` |

## Failure Reading

### `PORT_0022`

- MySQL:
  - `source.sql` executed
  - `rewrite_pos_01.sql` failed as written
  - blocker:
    - `CAST(... AS TIMESTAMP)` syntax is not accepted by MySQL in the positive rewrite
- Spark:
  - source failed before rewrite
  - blocker:
    - Spark rejects source-side `CAST(... AS DATETIME)` with `UNSUPPORTED_DATATYPE`

### `PORT_0024`

- MySQL:
  - source and rewrite both executed
  - exact bytes differed, but normalized TSV matched
- Spark:
  - source and rewrite both executed
  - exact bytes differed, but normalized TSV matched

Interpretation:

- `PORT_0024` is the only bounded cross-engine closure inside this run
- the existing normalized numeric policy was required and sufficient

### `PORT_0025`

- MySQL:
  - `source.sql` executed
  - `rewrite_pos_01.sql` failed as written
  - blocker:
    - `CAST(... AS TIMESTAMP)` syntax is not accepted by MySQL in the positive rewrite
- Spark:
  - source failed before rewrite
  - blocker:
    - Spark rejects source-side `CAST(... AS DATETIME)` with `UNSUPPORTED_DATATYPE`

## Artifact Paths

Top-level report:

- `reports/formal_expansion/port_cross_engine_bounded_execution_v0.json`

Case-local result checks:

- `cases/PORT/PORT_0022/runs/mysql/result_check.json`
- `cases/PORT/PORT_0022/runs/spark/result_check.json`
- `cases/PORT/PORT_0024/runs/mysql/result_check.json`
- `cases/PORT/PORT_0024/runs/spark/result_check.json`
- `cases/PORT/PORT_0025/runs/mysql/result_check.json`
- `cases/PORT/PORT_0025/runs/spark/result_check.json`

## Interpretation

This run does not support any claim of `6`-case PORT closure or final cross-engine matrix closure.

What it does support:

- a real bounded MySQL + Spark execution attempt was carried out on the approved `3`-case subset
- `PORT_0024` closed on both engines under the existing normalized numeric policy
- `PORT_0022` and `PORT_0025` remain blocked by engine-specific SQL compatibility:
  - MySQL positive rewrite incompatibility
  - Spark source-side `DATETIME` incompatibility

## Recommended Next Action

- keep the claim bounded
- if further work is approved later:
  - treat `PORT_0024` as bounded cross-engine success evidence
  - classify `PORT_0022` and `PORT_0025` as execution blockers rather than checker mismatches
  - do not widen to the excluded cases without a new approval step
