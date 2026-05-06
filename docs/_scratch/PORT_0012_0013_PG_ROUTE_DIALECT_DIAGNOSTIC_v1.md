# PORT_0012_0013_PG_ROUTE_DIALECT_DIAGNOSTIC_v1

## 0. Purpose And Boundary
This is a read-only diagnostic for `PORT_0012` and `PORT_0013` only. No DB execution, no SQLGlot or LLM route rerun, no checker/speedup, no `SpeedupTransferRate`, and no script/case/artifact modification were performed.

## 1. Current PORT Snapshot Recap
The bounded PG-side route subset remains `6`, and the bounded cross-engine closed subset is now `4`: `PORT_0004`, `PORT_0022`, `PORT_0024`, and `PORT_0025`. `PORT_0012` and `PORT_0013` remain PG-route blocked, and `SpeedupTransferRate` remains not computed.

## 2. Artifact Inventory
`PORT_0012`:
- source SQL: [cases/PORT/PORT_0012/source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0012/source.sql)
- positive rewrite: [cases/PORT/PORT_0012/rewrite_pos_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0012/rewrite_pos_01.sql)
- local case result check: [cases/PORT/PORT_0012/runs/result_check.json](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0012/runs/result_check.json)
- SQLGlot / LLM route evidence:
  - [reports/formal_port/port_current_results_snapshot_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_port/port_current_results_snapshot_v0.json)
  - [reports/formal_port/port_pg_consistency_diagnostic_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_port/port_pg_consistency_diagnostic_v0.json)
  - [reports/formal_port/llm_translate_port_0012_targeted_call_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_port/llm_translate_port_0012_targeted_call_v0.json)
  - [reports/formal_port/llm_translate_port_0012_targeted_pg_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_port/llm_translate_port_0012_targeted_pg_v0.json)
  - [reports/formal_port/llm_translate_port_0012_targeted_summary_v0.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_port/llm_translate_port_0012_targeted_summary_v0.json)
  - [reports/formal_port/result_checks/llm_direct_translate/port_0012.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_port/result_checks/llm_direct_translate/port_0012.json)
  - [reports/formal_port/result_checks/llm_direct_translate/port_0012_pg_normalized_reference.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_port/result_checks/llm_direct_translate/port_0012_pg_normalized_reference.json)

`PORT_0013`:
- source SQL: [cases/PORT/PORT_0013/source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0013/source.sql)
- positive rewrite: [cases/PORT/PORT_0013/rewrite_pos_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0013/rewrite_pos_01.sql)
- local case result check: [cases/PORT/PORT_0013/runs/result_check.json](/home/tianci_gao/code/sql-rewrite-bench/cases/PORT/PORT_0013/runs/result_check.json)
- SQLGlot / LLM route evidence:
  - [reports/formal_expansion/port_batch2c/result_checks/sqlglot_transpile/port_0013.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/port_batch2c/result_checks/sqlglot_transpile/port_0013.json)
  - [reports/formal_expansion/port_batch2c/result_checks/llm_direct_translate/port_0013.json](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/port_batch2c/result_checks/llm_direct_translate/port_0013.json)
  - [reports/formal_expansion/port_batch2c/result_materialization/llm_direct_translate/port_0013.tsv](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/port_batch2c/result_materialization/llm_direct_translate/port_0013.tsv)
  - [reports/formal_expansion/port_batch2c/result_materialization/reference/port_0013.tsv](/home/tianci_gao/code/sql-rewrite-bench/reports/formal_expansion/port_batch2c/result_materialization/reference/port_0013.tsv)

## 3. PORT_0012 Diagnostic
### SQLGlot Transpile route
The blocked PG-side route is `SQLGlot Transpile`. The exact failing surface is the transpiled SQL turning identifiers into string literals, especially:

```sql
TO_CHAR(CAST('birthday' AS TIMESTAMPTZ), 'YYYY') = '1980'
```

The same bad surface also appears around `'sex'`, `'id'`, and `'diagnosis'`. The recorded PostgreSQL failure is `InvalidDatetimeFormat` with `invalid input syntax for type timestamp with time zone: "birthday"`.

Classification: `pg_route_dialect_function_mismatch`

Likely minimal repair:
- bounded PG-route temp SQL repair only
- preserve canonical case SQL
- normalize the route execution surface so quoted identifiers remain identifiers and the datetime formatting expression stays PostgreSQL-compatible

Risk:
- medium to high, because the failure is not just one cast token; the route surface corrupts identifier semantics

### LLM Translate route
The targeted LLM route SQL itself executes on PostgreSQL successfully. The earlier checker failure was tied to an unnormalized PG reference surface using `AS DOUBLE` and `YEAR(...)`, not to the LLM SQL body. After using a PG-normalized reference, the LLM route is consistent.

This means the active blocker for `PORT_0012` is not the LLM route output. It is the SQLGlot PG-route surface plus the older reference normalization gap.

## 4. PORT_0013 Diagnostic
### SQLGlot Transpile route
The blocked PG-side route is `SQLGlot Transpile`. The exact failing surface is boolean aggregation lowered to:

```sql
SUM("t2"."gender" = 'F')
```

The recorded PostgreSQL failure is `UndefinedFunction` with `function sum(boolean) does not exist`.

Classification: `pg_route_boolean_aggregation_failure`

Likely minimal repair:
- bounded PG-route temp SQL repair only
- preserve canonical case SQL
- normalize the route execution surface to a PostgreSQL-safe equivalent such as `COUNT(CASE WHEN ... THEN 1 END)` or `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`

Risk:
- medium, but this is more localized than `PORT_0012`

### LLM Translate route
The LLM route is already checker-consistent for `PORT_0013`. The stored route result check shows no failure and matches the reference materialization.

This means the active blocker for `PORT_0013` is the SQLGlot PG-route surface, not the LLM route.

## 5. Cross-case / Cross-route Pattern
The failures are independent and route-specific.

- `PORT_0012` is a SQLGlot PG-route datetime and quoted-identifier surface failure.
- `PORT_0013` is a SQLGlot PG-route boolean aggregation lowering failure.

Both cases appear repairable through bounded PG-route temp SQL normalization rather than canonical source or rewrite file edits. The safer approach is route-surface repair, not case package modification.

`PORT_0012` is the riskier repair because the route output shows broader identifier-surface corruption. `PORT_0013` is narrower and more mechanical.

## 6. Recommended Fix Plan
Patch both route surfaces with temp SQL and rerun bounded PG-side route/checker.

More specifically:
- `PORT_0012`: patch the PG-route datetime / quoted-identifier surface only
- `PORT_0013`: patch the PG-route boolean aggregation surface only
- keep all repairs at the route execution surface or normalized temporary SQL level
- do not modify canonical `source.sql` or canonical positive rewrite files

## 7. Recommended Next Step
`patch both PORT_0012 / PORT_0013 PG-route surfaces and rerun bounded PG-side route/checker`

## 8. Non-Modification Note
Confirmed:
- no execution
- no SQLGlot or LLM route rerun
- no checker/speedup
- no `SpeedupTransferRate`
- no model/API
- no registry/review/rules/`EXECUTION_STATUS` changes
- no case/script/artifact modifications
- taxonomy notes untouched
