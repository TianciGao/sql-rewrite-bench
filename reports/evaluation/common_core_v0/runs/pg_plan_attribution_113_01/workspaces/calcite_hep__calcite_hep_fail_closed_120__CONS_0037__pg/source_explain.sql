set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_cons_0037_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT EMP.DEPTNO, COUNT(DISTINCT DEPT.NAME) FROM EMP LEFT JOIN DEPT ON EMP.DEPTNO = DEPT.DEPTNO GROUP BY EMP.DEPTNO;
rollback;
