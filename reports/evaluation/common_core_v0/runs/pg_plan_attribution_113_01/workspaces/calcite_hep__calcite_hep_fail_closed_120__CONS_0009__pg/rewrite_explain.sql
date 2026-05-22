set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_cons_0009_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT *
FROM "t0"
WHERE "t0a" < (SELECT SUM("c")
FROM (SELECT "t1c" AS "c"
FROM "t1"
WHERE "t1a" = "t0"."t0a"
UNION ALL
SELECT "t2c" AS "c"
FROM "t2"
WHERE "t2b" = "t0"."t0b") AS "t5");
rollback;
