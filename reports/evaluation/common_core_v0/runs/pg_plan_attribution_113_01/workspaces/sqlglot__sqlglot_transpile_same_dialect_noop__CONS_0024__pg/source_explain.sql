set search_path to attr113_sqlglot_sqlglot_transpile_same_dialect_noop_cons_002;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT empno
FROM emp AS e
LEFT JOIN dept AS d
  ON d.deptno = e.deptno
 AND EXISTS (
   SELECT e2.deptno
   FROM emp AS e2
   WHERE e2.deptno = d.deptno
   GROUP BY e2.deptno
   HAVING SUM(e2.sal) > 1000000
 );
rollback;
