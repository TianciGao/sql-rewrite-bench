set search_path to attr113_direct_llm_direct_llm_same_engine_rewrite_cons_0036_;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT NAME AS NAME, COUNT(*) AS C FROM DEPT GROUP BY NAME HAVING NAME = 'Charlie';
rollback;
