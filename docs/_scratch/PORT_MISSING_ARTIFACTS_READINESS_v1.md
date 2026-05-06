# PORT_MISSING_ARTIFACTS_READINESS_v1

## 0. Purpose And Boundary
- no-execution artifact readiness audit
- no DB/checker/speedup
- no SpeedupTransferRate
- not cross-engine closure yet

## 1. Source Preflight Recap
- bounded PG-side subset: `PORT_0004, PORT_0012, PORT_0022, PORT_0013, PORT_0024, PORT_0025`
- clean PG-side subset: `PORT_0004, PORT_0022`
- existing cross-engine closed subset: `PORT_0024`
- SpeedupTransferRate is not ready because aligned cross-engine executable, consistency, and target-engine benefit evidence is still incomplete

## 2. Required Closure Artifact Contract
- `postgresql_source_reference_route_artifacts`:
  - `reports/formal_port/result_materialization/reference/{case_id_lower}.tsv`
  - `reports/formal_port/result_checks/sqlglot_transpile/{case_id_lower}.json or reports/formal_port/result_checks/llm_direct_translate/{case_id_lower}.json`
  - `reports/formal_port/result_materialization/sqlglot_transpile/{case_id_lower}.tsv or reports/formal_port/result_materialization/llm_direct_translate/{case_id_lower}.tsv`
- `mysql_artifacts`:
  - `cases/PORT/{case_id}/schema/ddl_mysql.sql`
  - `cases/PORT/{case_id}/validation/mysql_witness_data.sql or standardized equivalent generated from existing loader`
  - `cases/PORT/{case_id}/runs/mysql/source.tsv`
  - `cases/PORT/{case_id}/runs/mysql/rewrite_pos_01.tsv`
  - `cases/PORT/{case_id}/runs/mysql/result_check.json`
  - `cases/PORT/{case_id}/runs/mysql/plans/source.json`
- `spark_artifacts`:
  - `cases/PORT/{case_id}/schema/ddl_spark.sql`
  - `cases/PORT/{case_id}/validation/spark_witness_data.sql or standardized equivalent generated from existing loader`
  - `cases/PORT/{case_id}/runs/spark/source.tsv`
  - `cases/PORT/{case_id}/runs/spark/rewrite_pos_01.tsv`
  - `cases/PORT/{case_id}/runs/spark/result_check.json`
  - `cases/PORT/{case_id}/runs/spark/plans/rewrite_pos_01.txt`
- `route_candidate_sql`:
  - `cases/PORT/{case_id}/rewrite_pos_01.sql`
  - `route-specific PG-side candidate capture if using SQLGlot or LLM route reports`
- `result_comparison_json`:
  - `cases/PORT/{case_id}/runs/mysql/result_check.json`
  - `cases/PORT/{case_id}/runs/spark/result_check.json`
  - `reports/formal_port/result_checks/<route>/{case_id_lower}.json`
- `closure_summary_json`:
  - `reports/formal_expansion/port_cross_engine_bounded_execution_v0.json or later bounded closure batch summary`

## 3. Per-case Artifact Inventory
| case_id | role_in_next_closure | pg_artifacts | mysql_artifacts | spark_artifacts | route_outputs | result_check_artifacts | missing_artifacts | execution_surface_failures | readiness_status | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PORT_0004 | artifact_first_closure_candidate | present | present | present | LLM_DIRECT_TRANSLATE | present | runs/mysql/result_check.json, runs/spark/result_check.json, validation/mysql_witness_data.sql, validation/spark_witness_data.sql | none | missing_mysql_witness_contract | create standardized mysql/spark witness artifacts from existing loader drafts without changing case semantics |
| PORT_0022 | execution_failure_followup_candidate | present | present | present | LLM_DIRECT_TRANSLATE | present | none | mysql:TIMESTAMP_surface, mysql:rewrite_execution_failed, spark:DATETIME_surface, spark:source_execution_failed | previous_target_engine_failure_needs_diagnosis | diagnose target-engine SQL surface before any rerun |
| PORT_0024 | existing_cross_engine_anchor | present | present | present | case-local only | present | none | none | already_cross_engine_closed_anchor | preserve as read-only anchor |
| PORT_0025 | execution_failure_followup_candidate | present | present | present | case-local only | present | none | mysql:TIMESTAMP_surface, mysql:rewrite_execution_failed, spark:DATETIME_surface, spark:source_execution_failed | previous_target_engine_failure_needs_diagnosis | diagnose target-engine SQL surface before any rerun |

## 4. Case-specific Notes
### PORT_0004
- PG-side route artifacts exist in `reports/formal_port` and local PG draft outputs exist under `runs/pg/`.
- MySQL and Spark use loader-style witness drafts (`load_witness_mysql.sql`, `load_witness_spark.sql`) instead of the standardized `mysql_witness_data.sql` / `spark_witness_data.sql` contract used by the bounded closure packet.
- This is an artifact-contract gap, not yet an engine-surface failure.

### PORT_0022
- Artifact surface is already present for MySQL and Spark, including witness SQL, result checks, logs, and TSV outputs.
- Prior bounded execution failed on target-engine SQL surface: MySQL rewrite execution hit `TIMESTAMP` syntax trouble and Spark source execution failed on `DATETIME`.

### PORT_0024
- Remains the existing cross-engine closed anchor with successful MySQL and Spark execution plus consistent result checks.
- No artifact creation is needed; preserve as read-only anchor evidence.

### PORT_0025
- Artifact surface is already present for MySQL and Spark.
- Prior bounded execution failed on the same target-engine SQL surface pattern as `PORT_0022`: MySQL rewrite syntax around `TIMESTAMP`, Spark source failure on `DATETIME`.

## 5. Proposed Next Batch
- cases: `['PORT_0004']`
- engines: `['MySQL', 'Spark']`
- route(s): `['SQLGlot Transpile', 'LLM Translate']`
- artifact creation or execution next: `artifact_creation_only`
- why minimal: `PORT_0004 is the only focus case blocked by standardized closure-packet witness artifacts rather than already-demonstrated engine-surface failures`

## 6. Recommended Next Step
- `create PORT_0004 closure artifact bundle`

## 7. Non-Modification Note
- no execution
- no DB/checker/speedup
- no model/API
- no SpeedupTransferRate
- no registry/review/rules/EXECUTION_STATUS changes
- taxonomy notes untouched
