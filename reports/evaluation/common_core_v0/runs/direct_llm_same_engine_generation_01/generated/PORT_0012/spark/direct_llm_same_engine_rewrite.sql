SELECT CAST( SUM( CASE WHEN "sex" = 'F' THEN 1 ELSE 0 END ) AS REAL ) * 100 / NULLIF( COUNT( "id" ), 0 ) FROM "patient" WHERE "diagnosis" = 'RA' AND YEAR("birthday") = 1980
