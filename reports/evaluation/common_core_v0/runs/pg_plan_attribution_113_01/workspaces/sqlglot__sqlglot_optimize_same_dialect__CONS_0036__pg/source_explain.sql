set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_cons_0036_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT NAME AS NAME, COUNT(*) AS C FROM DEPT GROUP BY NAME HAVING NAME = 'Charlie';
rollback;
