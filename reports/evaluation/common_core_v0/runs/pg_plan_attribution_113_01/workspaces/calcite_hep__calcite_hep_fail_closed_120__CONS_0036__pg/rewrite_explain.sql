set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_cons_0036_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT "name", COUNT(*) AS "c"
FROM "dept"
GROUP BY "name"
HAVING "name" = 'Charlie';
rollback;
