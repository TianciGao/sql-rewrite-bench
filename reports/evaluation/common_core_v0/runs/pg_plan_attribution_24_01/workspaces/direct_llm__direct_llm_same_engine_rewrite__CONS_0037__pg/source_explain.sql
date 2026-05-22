set search_path to attr24_direct_llm__direct_llm_same_engine_rewrite__cons_0037;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT EMP.DEPTNO, COUNT(DISTINCT DEPT.NAME) FROM EMP LEFT JOIN DEPT ON EMP.DEPTNO = DEPT.DEPTNO GROUP BY EMP.DEPTNO;
rollback;
