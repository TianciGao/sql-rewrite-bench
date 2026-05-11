set search_path to attr24_sqlglot__sqlglot_optimize_same_dialect__cons_0037__pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT EMP.DEPTNO, COUNT(DISTINCT DEPT.NAME) FROM EMP LEFT JOIN DEPT ON EMP.DEPTNO = DEPT.DEPTNO GROUP BY EMP.DEPTNO;
rollback;
