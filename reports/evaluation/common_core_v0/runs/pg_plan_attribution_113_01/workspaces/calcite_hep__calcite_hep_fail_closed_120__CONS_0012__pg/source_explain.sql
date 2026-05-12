set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_cons_0012_pg;
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
