set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_port_0012_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT CAST( SUM( CASE WHEN "sex" = 'F' THEN 1 ELSE 0 END ) AS REAL ) * 100 / NULLIF( COUNT( "id" ) , 0 ) FROM "patient" WHERE "diagnosis" = 'RA' AND TO_CHAR( CAST( "birthday" AS TIMESTAMP ) , 'YYYY' ) = '1980';
rollback;
