set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_cons_0037_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT EMP.DEPTNO, COUNT(DISTINCT DEPT.NAME) FROM EMP LEFT JOIN DEPT ON EMP.DEPTNO = DEPT.DEPTNO GROUP BY EMP.DEPTNO;
rollback;
