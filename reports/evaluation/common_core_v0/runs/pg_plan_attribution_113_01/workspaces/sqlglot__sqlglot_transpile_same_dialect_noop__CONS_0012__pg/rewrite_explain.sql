set search_path to attr113_sqlglot_sqlglot_transpile_same_dialect_noop_cons_001;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT
  *
FROM dept AS d
WHERE
  EXISTS(
    SELECT
      *
    FROM emp AS e
    WHERE
      e.deptno = d.deptno
    LIMIT 1
    OFFSET 2
  );
rollback;
