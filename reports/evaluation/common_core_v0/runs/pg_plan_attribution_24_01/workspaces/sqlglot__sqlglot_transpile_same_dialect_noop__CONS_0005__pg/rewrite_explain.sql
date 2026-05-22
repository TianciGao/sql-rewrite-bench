set search_path to attr24_sqlglot__sqlglot_transpile_same_dialect_noop__cons_00;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT
  i,
  j
FROM table1
WHERE
  NOT table1.j IN (
    SELECT
      i
    FROM table2
    WHERE
      table1.i = table2.j
  );
rollback;
