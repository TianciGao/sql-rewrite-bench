set search_path to attr113_sqlglot_sqlglot_transpile_same_dialect_noop_cons_000;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT i, j
FROM table1
WHERE table1.j NOT IN (
  SELECT i
  FROM table2
  WHERE table1.i = table2.j
);
rollback;
