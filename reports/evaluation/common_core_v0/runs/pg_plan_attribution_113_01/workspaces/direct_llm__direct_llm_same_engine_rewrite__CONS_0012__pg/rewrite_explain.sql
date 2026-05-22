set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_cons_0012_;
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
