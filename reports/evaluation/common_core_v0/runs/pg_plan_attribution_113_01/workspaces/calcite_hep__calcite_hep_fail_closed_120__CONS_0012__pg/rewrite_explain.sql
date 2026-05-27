set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_cons_0012_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT *
FROM "dept"
WHERE EXISTS (SELECT "empno", "ename", "job", "mgr", "hiredate", "sal", "comm", "deptno"
FROM "emp"
WHERE "deptno" = "dept"."deptno"
OFFSET 2 ROWS
FETCH NEXT 1 ROWS ONLY);
rollback;
