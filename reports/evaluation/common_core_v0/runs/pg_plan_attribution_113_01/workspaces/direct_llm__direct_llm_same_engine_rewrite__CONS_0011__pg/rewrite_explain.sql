set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_cons_0011_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT E1.ENAME
FROM emp E1
WHERE EXISTS (
  SELECT 1
  FROM dept D
  LEFT JOIN bonus B
    ON D.dname = B.ename
   AND B.job = E1.job
  WHERE B.ename IS NULL
);
rollback;
