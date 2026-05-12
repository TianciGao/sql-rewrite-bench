set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_cons_0005_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT i, j
FROM table1
WHERE j NOT IN (
  SELECT i
  FROM table2
  WHERE table1.i = table2.j
);
rollback;
