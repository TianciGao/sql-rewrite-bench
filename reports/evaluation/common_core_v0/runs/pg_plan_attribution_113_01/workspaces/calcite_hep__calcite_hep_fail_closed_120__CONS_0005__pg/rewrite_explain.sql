set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_cons_0005_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT *
FROM "table1"
WHERE "j" NOT IN (SELECT "i"
FROM "table2"
WHERE "table1"."i" = "j");
rollback;
