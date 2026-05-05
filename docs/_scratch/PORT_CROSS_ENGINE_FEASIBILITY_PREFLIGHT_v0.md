# PORT_CROSS_ENGINE_FEASIBILITY_PREFLIGHT_v0

## Scope

- Packet:
  - `PORT_0004`
  - `PORT_0012`
  - `PORT_0022`
  - `PORT_0013`
  - `PORT_0024`
  - `PORT_0025`
- Boundary:
  - preflight only
  - no MySQL execution
  - no Spark execution
  - no PostgreSQL execution
  - no SQLGlot generation
  - no model calls
  - not cross-engine closure

## Summary

Current bounded cross-engine readiness result:

- `case_count=6`
- `mysql_ready_count=3`
- `spark_ready_count=3`
- `both_engine_ready_count=3`
- `blocked_count=3`

Recommended bounded MySQL+Spark execution subset:

- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

## Per-Case Readiness

| case_id | mysql_ready | spark_ready | main blockers | recommended next action |
| --- | --- | --- | --- | --- |
| `PORT_0004` | no | no | `missing_witness_data` under the standardized `*_witness_data.sql` contract; only loader-style witness files exist | keep as preflight-only until witness-file contract is normalized for MySQL and Spark |
| `PORT_0012` | no | no | `datetime_formatting`, `dialect_functions` | keep blocked for bounded cross-engine execution; this remains a holdout / failure-analysis case rather than a clean cross-engine candidate |
| `PORT_0022` | yes | yes | none in current preflight | candidate for bounded MySQL+Spark execution subset |
| `PORT_0013` | no | no | `boolean_aggregation` | keep blocked until boolean-aggregation portability semantics are explicitly handled |
| `PORT_0024` | yes | yes | none in current preflight | candidate for bounded MySQL+Spark execution subset |
| `PORT_0025` | yes | yes | none in current preflight | candidate for bounded MySQL+Spark execution subset |

## Artifact Reading

What was present across the packet:

- all six cases have:
  - `source.sql`
  - `rewrite_pos_01.sql`
  - `schema/ddl_pg.sql`
  - `schema/ddl_mysql.sql`
  - `schema/ddl_spark.sql`
  - PostgreSQL-side `runs/result_check.json`
- `PORT_0012`, `PORT_0022`, `PORT_0013`, `PORT_0024`, and `PORT_0025` have:
  - `validation/pg_witness_data.sql`
  - `validation/mysql_witness_data.sql`
  - `validation/spark_witness_data.sql`
- `PORT_0004` is the outlier:
  - it has loader-style witness files such as `load_witness_mysql.sql` and `load_witness_spark.sql`
  - but not the standardized `mysql_witness_data.sql` / `spark_witness_data.sql` / `pg_witness_data.sql` naming expected by this preflight

Checker / policy state:

- `PORT_0004` has case-local `validation/checker.yaml`
- `PORT_0012` relies on existing report-local portability policy notes rather than a case-local checker file
- `PORT_0022` relies on existing diagnostic / closeout notes rather than a case-local checker file
- `PORT_0013`, `PORT_0024`, and `PORT_0025` rely on [BATCH2C_PORT_REFERENCE_CHECKER_POLICY_v0.md](/home/tianci_gao/code/sql-rewrite-bench/docs/_scratch/BATCH2C_PORT_REFERENCE_CHECKER_POLICY_v0.md)

## Blocker Reading

The current blockers line up with already-known portability trouble spots:

- `PORT_0012`
  - `TO_CHAR(...)`, `YEAR(...)`, and date-format portability remain the dominant blocker family
- `PORT_0013`
  - boolean aggregation remains the dominant blocker family
- `PORT_0004`
  - the case is structurally promising, but the witness-file contract is not aligned with the other five cases yet

Secondary caveats that are not currently blocking the recommended subset:

- `PORT_0024` still carries numeric-formatting risk
- `PORT_0025` still carries date/time-function normalization risk
- none of the six cases currently have MySQL- or Spark-side `result_check.json` artifacts; this preflight treats that as expected absence before execution, not as a blocker by itself

## Interpretation

This is enough to justify a bounded next step, but not a broad claim:

- a bounded MySQL+Spark follow-up appears feasible on `PORT_0022`, `PORT_0024`, and `PORT_0025`
- `PORT_0004`, `PORT_0012`, and `PORT_0013` should remain outside that first bounded cross-engine slice for now
- the current six-case PORT packet still does not justify any claim of cross-engine closure

## Execute Refusal

`--execute` is intentionally refused for this command and writes:

- `reports/formal_expansion/port_cross_engine_feasibility_preflight_execute_refused_v0.json`

That keeps this step read-only and prevents accidental engine execution during feasibility auditing.
