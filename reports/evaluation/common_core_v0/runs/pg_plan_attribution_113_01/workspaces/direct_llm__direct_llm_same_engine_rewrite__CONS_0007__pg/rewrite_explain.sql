set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_cons_0007_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT *
FROM tmp_emps e1
WHERE EXISTS (
  SELECT 1
  FROM tmp_emps e2
  WHERE e2.commission = e1.commission
  AND e2.deptno <> e1.deptno
);
rollback;
