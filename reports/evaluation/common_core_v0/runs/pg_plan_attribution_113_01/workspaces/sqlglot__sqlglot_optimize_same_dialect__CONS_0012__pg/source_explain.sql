set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_cons_0012_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT *
FROM dept d
WHERE EXISTS (
  SELECT *
  FROM emp e
  WHERE e.deptno = d.deptno
  LIMIT 1 OFFSET 2
);
rollback;
