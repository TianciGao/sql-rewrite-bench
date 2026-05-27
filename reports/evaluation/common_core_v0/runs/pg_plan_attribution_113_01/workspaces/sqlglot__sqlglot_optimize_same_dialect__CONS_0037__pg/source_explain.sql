set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_cons_0037_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT EMP.DEPTNO, COUNT(DISTINCT DEPT.NAME) FROM EMP LEFT JOIN DEPT ON EMP.DEPTNO = DEPT.DEPTNO GROUP BY EMP.DEPTNO;
rollback;
