# PORT_CROSS_ENGINE_CLOSEOUT_v0

## Status

This is a paper-facing PORT cross-engine closeout note for wording control and evidence consolidation only.

It does not record a new experiment, does not perform registry writeback, and does not imply admission, promotion, or common-core movement.

## Scope And Source Basis

Sources read for this note:

- `docs/_scratch/PORT_CROSS_ENGINE_FEASIBILITY_PREFLIGHT_v0.md`
- `reports/formal_expansion/port_cross_engine_feasibility_preflight_v0.json`
- `reports/formal_expansion/port_cross_engine_feasibility_preflight_execute_refused_v0.json`
- `docs/_scratch/PORT_CROSS_ENGINE_BOUNDED_EXECUTION_v0.md`
- `reports/formal_expansion/port_cross_engine_bounded_execution_v0.json`
- `cases/PORT/PORT_0022/runs/mysql/result_check.json`
- `cases/PORT/PORT_0022/runs/spark/result_check.json`
- `cases/PORT/PORT_0024/runs/mysql/result_check.json`
- `cases/PORT/PORT_0024/runs/spark/result_check.json`
- `cases/PORT/PORT_0025/runs/mysql/result_check.json`
- `cases/PORT/PORT_0025/runs/spark/result_check.json`
- existing paper-facing drafts:
  - `docs/_scratch/FORMAL_PORT_RESULTS_CLOSEOUT_v0.md`
  - `docs/_scratch/EXPANDED_PORT_RESULTS_CLOSEOUT_v0.md`

## A. PG-side PORT evidence

- denominator: `6` PORT cases
- SQLGlot Transpile: PG-side only, partial success
- LLM Translate: PG-side only, current bounded slice
- claim boundary: PostgreSQL-side portability evidence only, not cross-engine closure

Interpretation:

- the current PG-facing evidence base is the already expanded `6`-case PORT packet
- this layer should remain separated from later MySQL / Spark evidence
- PG-side execution and PG-side checker closure do not by themselves establish cross-engine closure

## B. Cross-engine feasibility preflight

- denominator: `6` PORT cases
- `mysql_ready_count=3`
- `spark_ready_count=3`
- `both_engine_ready_count=3`
- recommended bounded execution subset:
  - `PORT_0022`
  - `PORT_0024`
  - `PORT_0025`
- blocked before execution:
  - `PORT_0004`: witness-file contract not normalized
  - `PORT_0012`: datetime_formatting / dialect_functions
  - `PORT_0013`: boolean_aggregation
- claim boundary: `preflight_only_not_cross_engine_closure`

Interpretation:

- this layer is a read-only readiness screen across the `6`-case packet
- the execute-refused report confirms that the preflight step itself was not an execution run
- readiness should not be restated as closure

## C. Bounded MySQL+Spark execution attempt

- denominator: `3` approved cases x `2` engines
- cases:
  - `PORT_0022`
  - `PORT_0024`
  - `PORT_0025`
- MySQL execution occurred: yes
- Spark execution occurred: yes
- PostgreSQL execution occurred: no
- model calls: no
- SQLGlot: no
- claim boundary:
  - `bounded_3_case_mysql_spark_execution_not_full_port_closure`

“A bounded 3-case MySQL+Spark execution attempt was recorded for PORT_0022, PORT_0024, and PORT_0025. Only PORT_0024 closed on both engines under the existing normalized numeric policy. PORT_0022 and PORT_0025 remain execution-blocked before checker comparison. This is not full PORT closure and not a final cross-engine matrix.”

## D. Actual bounded result

- `mysql_execution_success_count=1`
- `mysql_consistency_success_count=1`
- `spark_execution_success_count=1`
- `spark_consistency_success_count=1`
- `both_engine_execution_success_count=1`
- `both_engine_consistency_success_count=1`
- only `PORT_0024` closed on both engines
- `PORT_0024` required existing normalized numeric policy
- `PORT_0022` and `PORT_0025` remain execution-blocked before checker comparison

Interpretation:

- the bounded result is actual execution evidence, but only inside the approved `3`-case subset
- the only both-engine bounded success is `PORT_0024`
- the normalized numeric policy is part of the accepted reading for `PORT_0024`, not a new governance action in this note

## E. Failure classification

- `PORT_0022` / MySQL:
  - `rewrite_execution_failed` due MySQL rejecting positive rewrite near `CAST(... AS TIMESTAMP)`
- `PORT_0022` / Spark:
  - `source_execution_failed` due Spark rejecting source-side `CAST(... AS DATETIME)`
- `PORT_0025` / MySQL:
  - `rewrite_execution_failed` due MySQL rejecting positive rewrite near `CAST(... AS TIMESTAMP)`
- `PORT_0025` / Spark:
  - `source_execution_failed` due Spark rejecting source-side `CAST(... AS DATETIME)`
- These are execution blockers, not checker mismatches.

Interpretation:

- the failed pairs did not reach a checker comparison stage
- they should be described as execution-blocked engine/case pairs rather than inconsistency results

## F. Claim boundaries

Accepted wording:

“A bounded 3-case MySQL+Spark execution attempt was recorded for PORT_0022, PORT_0024, and PORT_0025. Only PORT_0024 closed on both engines under the existing normalized numeric policy. PORT_0022 and PORT_0025 remain execution-blocked before checker comparison. This is not full PORT closure and not a final cross-engine matrix.”

Exact claim boundary:

- `bounded_3_case_mysql_spark_execution_not_full_port_closure`

Supporting boundary layers that must remain explicit:

- PG-side layer:
  - PostgreSQL-side portability evidence only, not cross-engine closure
- preflight layer:
  - `preflight_only_not_cross_engine_closure`
- bounded execution layer:
  - `bounded_3_case_mysql_spark_execution_not_full_port_closure`

## G. Forbidden wording

Do not describe the current evidence as any of the following:

- `PORT cross-engine closure`
- `full cross-engine matrix`
- `6-case PORT closure`
- `final portability closure`
- `all approved cases closed`
- `MySQL and Spark portability proven`
- `final cross-engine evidence for the PORT packet`
- anything implying registry/admission/common-core promotion

## Non-Modification Note

- no DB execution was performed while producing this note
- no model calls were performed while producing this note
- no SQLGlot execution was performed while producing this note
- no case files were modified
- no `result_check.json` files were modified
- no report JSON files were modified
- no registry files were modified
- no review files were modified
- no benchmark rules, taxonomy rules, admission rules, or `docs/EXECUTION_STATUS.md` were modified
- the three long-standing untracked taxonomy notes were left untouched
