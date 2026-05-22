set search_path to attr24_direct_llm__direct_llm_same_engine_rewrite__cons_0012;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT *
FROM dept d
WHERE EXISTS (
  SELECT 1
  FROM emp e
  WHERE e.deptno = d.deptno
  LIMIT 1 OFFSET 2
);
rollback;
