# SQLSOLVER_ADAPTER_PREFLIGHT_CONS_0007_0035_v1

## 0. Purpose And Boundary
State:
- SQLSolver no-execution adapter preflight
- support/verifier only
- not rewrite generation
- not speedup
- not leaderboard

## 1. SQLSolver Substrate
Report:
- repo path: `/tmp/rewritebench_sqlsolver_audit/candidate`
- commit: `dcc2a91d8971a4c4d30b055f99d7d8428a1b754b`
- entrypoint: `sqlsolver.api.Entry`
- build contract visible: yes, `build.gradle`
- solver deps visible: yes, bundled Z3 libraries under `lib/`
- verdict contract: `EQ`, `NEQ`, `UNKNOWN`, `TIMEOUT`

## 2. Case Inventory
For `CONS_0007`:
- case root: [cases/CONS/CONS_0007](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007)
- source SQL path: [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/source.sql)
- positive SQL path: [rewrite_pos_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/rewrite_pos_01.sql)
- negative SQL path: [rewrite_neg_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/rewrite_neg_01.sql)
- schema path: [schema/ddl_pg.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/schema/ddl_pg.sql)
- control evidence present: [runs/pg/result_check.json](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/runs/pg/result_check.json), [runs/result_check.json](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0007/runs/result_check.json)
- files found/missing: all required files found

For `CONS_0035`:
- case root: [cases/CONS/CONS_0035](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0035)
- source SQL path: [source.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0035/source.sql)
- positive SQL path: [rewrite_pos_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0035/rewrite_pos_01.sql)
- negative SQL path: [rewrite_neg_01.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0035/rewrite_neg_01.sql)
- schema path: [schema/ddl_pg.sql](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0035/schema/ddl_pg.sql)
- control evidence present: [runs/pg/result_check.json](/home/tianci_gao/code/sql-rewrite-bench/cases/CONS/CONS_0035/runs/pg/result_check.json)
- files found/missing: all required files found

## 3. Adapter Bundle
For `CONS_0007`:
- temp bundle path: `/tmp/rewritebench_sqlsolver_adapter_preflight/CONS_0007`
- `sql1_positive.sql`: yes
- `sql2_positive.sql`: yes
- `sql1_negative.sql`: yes
- `sql2_negative.sql`: yes
- `schema.sql`: yes
- `expected_verdicts.json`: yes
- `future_command_NOT_RUN.txt`: yes
- `output_verdict_contract.md`: yes

For `CONS_0035`:
- temp bundle path: `/tmp/rewritebench_sqlsolver_adapter_preflight/CONS_0035`
- `sql1_positive.sql`: yes
- `sql2_positive.sql`: yes
- `sql1_negative.sql`: yes
- `sql2_negative.sql`: yes
- `schema.sql`: yes
- `expected_verdicts.json`: yes
- `future_command_NOT_RUN.txt`: yes
- `output_verdict_contract.md`: yes

## 4. Contract Gaps
For `CONS_0007`:
- schema/constraint gap: only bare DDL is bundled; no explicit PK/FK/UNIQUE bridge has been derived for SQLSolver yet
- SQL dialect gap: Calcite-family correlated `EXISTS` / nested subquery shape may stress SQLSolver support
- unsupported feature risk: correlated subquery handling is the main static risk
- verdict granularity gap: SQLSolver `UNKNOWN` does not separate unsupported SQL from parser failure
- timeout policy gap: no pinned wrapper timeout or timeout-to-metric policy yet

For `CONS_0035`:
- schema/constraint gap: only bare DDL is bundled; no explicit PK/FK/UNIQUE bridge has been derived for SQLSolver yet
- SQL dialect gap: aggregate and `NULL` semantics must align with SQLSolver’s supported subset
- unsupported feature risk: `COUNT(MGR)` vs scalar `CASE` rewrite needs aggregate/null-support confirmation
- verdict granularity gap: SQLSolver `UNKNOWN` does not separate unsupported SQL from parser failure
- timeout policy gap: no pinned wrapper timeout or timeout-to-metric policy yet

## 5. Future Smoke Readiness
For `CONS_0007`:
- readiness: `adapter_preflight_ready_not_executed`

For `CONS_0035`:
- readiness: `adapter_preflight_ready_not_executed`

## 6. Recommended Next Step
Choose exactly one:
- `implement SQLSolver runner dry-run for CONS_0007 / CONS_0035`

## 7. Non-Modification Note
Confirm no execution/build/install/DB/checker/speedup and no case/registry/review/rules/EXECUTION_STATUS changes.
