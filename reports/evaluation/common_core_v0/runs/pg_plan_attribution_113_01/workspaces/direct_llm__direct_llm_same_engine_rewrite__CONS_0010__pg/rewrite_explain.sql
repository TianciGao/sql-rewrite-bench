set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_cons_0010_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT E1.*
FROM emp E1
WHERE NOT EXISTS (
  SELECT 1
  FROM emp E2
  JOIN bonus B
    ON E2.sal = E1.sal
   AND B.job = E1.job
  WHERE E2.empno <> E1.empno
);
rollback;
