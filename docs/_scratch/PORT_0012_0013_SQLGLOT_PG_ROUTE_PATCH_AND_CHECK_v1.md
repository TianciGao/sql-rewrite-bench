# PORT_0012_0013_SQLGLOT_PG_ROUTE_PATCH_AND_CHECK_v1

## 0. Purpose And Boundary
- PORT_0012 / PORT_0013 only
- SQLGlot PG-route temp SQL patch + PG-side checker rerun
- no SQLGlot generation rerun
- no LLM rerun
- no MySQL/Spark
- no speedup
- no SpeedupTransferRate
- no canonical SQL edits

## 1. Prior Diagnostic Recap
- PORT_0012 SQLGlot quoted-identifier/datetime surface failure
- PORT_0013 SQLGlot boolean aggregation failure
- LLM route is not active blocker for either case

## 2. Patch Summary
### PORT_0012
- temp SQL path: `/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0012/sqlglot_pg_route_patched.sql`
- exact bad surface: `quoted identifiers corrupted into string literals around birthday/sex/id/diagnosis`
- exact normalized surface: `CAST("birthday" AS TIMESTAMPTZ) with identifier-preserving WHERE/COUNT surfaces`
- transformation: `repaired quoted-identifier corruption in SQLGlot preview: 'sex'->"sex", COUNT('id')->COUNT("id"), 'diagnosis'->"diagnosis", CAST('birthday' AS TIMESTAMPTZ)->CAST("birthday" AS TIMESTAMPTZ)`
- why canonical case SQL was not modified: temp-route normalization only
- risk: `medium_high`

### PORT_0013
- temp SQL path: `/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0013/sqlglot_pg_route_patched.sql`
- exact bad surface: `SUM("t2"."gender" = 'F')`
- exact normalized surface: `SUM(CASE WHEN "t2"."gender" = 'F' THEN 1 ELSE 0 END)`
- transformation: `replaced SUM("t2"."gender" = 'F') with SUM(CASE WHEN "t2"."gender" = 'F' THEN 1 ELSE 0 END) and normalized DOUBLE to DOUBLE PRECISION on a temp SQL surface`
- why canonical case SQL was not modified: temp-route normalization only
- risk: `medium`

## 3. PG-side Checker Rerun Results
| case_id | route | temp_sql_path | source_execution_status | candidate_execution_status | checker_status | consistency_status | failure_category | failure_summary | artifact_paths |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PORT_0012 | SQLGLOT_TRANSPILE | `/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0012/sqlglot_pg_route_patched.sql` | `success` | `success` | `consistent` | `consistent` | `none` | `` | `reference_tsv_path=/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0012/reference.tsv, candidate_tsv_path=/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0012/candidate.tsv, temp_sql_path=/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0012/sqlglot_pg_route_patched.sql, checker_output_path=/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0012/checker_result.json` |
| PORT_0013 | SQLGLOT_TRANSPILE | `/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0013/sqlglot_pg_route_patched.sql` | `success` | `success` | `consistent` | `consistent` | `none` | `` | `reference_tsv_path=/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0013/reference.tsv, candidate_tsv_path=/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0013/candidate.tsv, temp_sql_path=/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0013/sqlglot_pg_route_patched.sql, checker_output_path=/tmp/rewritebench_port_sqlglot_pg_route_patch/PORT_0013/checker_result.json` |

## 4. Updated Bounded PG-side Route Status
- PORT_0012 SQLGlot PG-route closed yes/no: `yes`
- PORT_0013 SQLGlot PG-route closed yes/no: `yes`
- bounded PG-side route packet status after this task: `port_0012_and_port_0013_closed`
- do not claim cross-engine closure yet

## 5. SpeedupTransferRate Status
- not_computed
- still not ready
- this task only addresses PG-side route blockers

## 6. Recommended Next Step
- `update PORT cross-engine closure snapshot with PG-route repair status`

## 7. Non-Modification Note
- no SQLGlot generation rerun
- no LLM route rerun
- no MySQL/Spark
- no speedup
- no SpeedupTransferRate
- no registry/review/rules/EXECUTION_STATUS changes
- taxonomy notes untouched
